#!/usr/bin/env python3
"""
作用：校验文章图片，按内容去重上传个人 GitHub 图床，再替换已验证的链接
Usage: python scripts/images.py prepare|upload|apply
Options: prepare 只下载与核验；upload 向图床提交缺失图片；apply 仅替换已验证图片
Description: 读取 gh 的登录身份，不保存或输出令牌；缓存位于 .migration-cache
             upload 会更新 SHERlocked93/pic 的 master；apply 会修改 Docs 和 README
"""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import json
import re
import subprocess
import threading
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

import requests

from archive import CACHE, ROOT, save_json
from reconcile import blocks, clean_promotion

# 图床路径以文章引用所使用的个人仓库为准
REPO = "SHERlocked93/pic"
RAW = f"https://raw.githubusercontent.com/{REPO}/master/"
IMAGE_PATTERN = re.compile(r'!\[[^\]\n]*\]\(([^\n]+?)\)|<img\b[^>]*?\bsrc=["\']([^"\']+)["\'][^>]*>', re.I)


def image_urls(text: str) -> list[str]:
    """只扫描非代码块中的实际图片引用"""
    result = []
    for block in blocks(text):
        if re.match(r"^\s*(`{3,}|~{3,})", block):
            continue
        block = re.sub(r"(`+)[^`\n]*\1", "", block)
        for match in IMAGE_PATTERN.finditer(block):
            value = (match[1] or match[2]).strip()
            if value.startswith("<") and ">" in value:
                value = value[1:value.index(">")]
            else:
                value = re.split(r'\s+["\']', value, maxsplit=1)[0]
            result.append(value)
    return result


def canonical(url: str) -> str:
    """还原个人图床的 CDN 地址及 GitHub 图片预览地址"""
    url = url.replace("&amp;", "&")
    match = re.match(r"https?://(?:cdn|fastly|testingcf|gcore)\.jsdelivr\.net/gh/SHERlocked93/pic@(?:master|main)/(.*)", url, re.I)
    if match:
        return RAW + quote(unquote(match[1]), safe="/")
    match = re.match(r"https?://github\.com/SHERlocked93/pic/(?:blob|raw)/master/(.*?)(?:\?raw=true)?$", url, re.I)
    if match:
        return RAW + quote(unquote(match[1]), safe="/")
    if url.lower().startswith(RAW.lower()):
        return RAW + quote(unquote(url[len(RAW):]), safe="/")
    return url


class GitHub:
    """只向 GitHub API 发送认证信息，图片下载使用独立无认证请求"""

    def __init__(self) -> None:
        """认证由 gh 管理，兼容未提供 auth token 子命令的旧版 CLI"""
        subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True, check=True)

    def api(self, endpoint: str, payload: dict | None = None, method: str | None = None) -> dict:
        """执行目标仓库的 GitHub API 请求，错误中不包含请求头"""
        command = ["gh", "api", endpoint]
        if payload is not None:
            command += ["-X", method or "POST", "--input", "-"]
        result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
            capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise RuntimeError(result.stderr.strip())
        return json.loads(result.stdout)

    def tree(self) -> dict:
        """读取完整图床目录，截断时拒绝进行不完整去重"""
        tree = self.api(f"repos/{REPO}/git/trees/master?recursive=1")
        if tree.get("truncated"):
            raise ValueError("图床目录被截断")
        return tree


def image_type(data: bytes) -> str:
    """校验文件签名，拒绝把访问拦截页作为图片上传"""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "webp"
    if data.startswith(b"BM"):
        return "bmp"
    if b"<svg" in data[:1000] and b"<html" not in data[:1000].lower():
        return "svg"
    if data[4:12] in {b"ftypavif", b"ftypavis"}:
        return "avif"
    raise ValueError("响应不是可识别的图片")


def download(url: str) -> tuple[bytes, str]:
    """缓存下载原图，保留动图的原始字节"""
    path = CACHE / "images" / (hashlib.sha256(url.encode()).hexdigest() + ".bin")
    if path.exists():
        data = path.read_bytes()
    else:
        if not url.startswith(("http://", "https://")):
            raise ValueError("原图为不可达的本地路径")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
        response.raise_for_status()
        data = response.content
        image_type(data)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(f'.{threading.get_ident()}.tmp')
        temporary.write_bytes(data)
        temporary.replace(path)
    return data, image_type(data)


def prepare() -> None:
    """找到可以校验的原图或同篇平台版本，不修改文章"""
    github = GitHub()
    tree = github.tree()
    save_json(CACHE / "picture-tree.json", tree)
    by_name, by_sha = defaultdict(list), {}
    for item in tree["tree"]:
        if item["type"] == "blob":
            by_name[Path(item["path"]).name].append(item["path"])
            by_sha[item["sha"]] = item["path"]
    alternatives = defaultdict(list)
    groups = json.loads((CACHE / "groups.json").read_text())
    for group in groups:
        local_images = image_urls(clean_promotion(group["local"]))
        for source in group["sources"]:
            remote_images = image_urls(clean_promotion(source["markdown"]))
            if len(local_images) == len(remote_images):
                for old, new in zip(local_images, remote_images):
                    if old != new:
                        alternatives[old].append(new)
    files = [ROOT / "README.md", *sorted((ROOT / "Docs").glob("*.md"))]
    urls = list(dict.fromkeys(url for file in files for url in image_urls(file.read_text())))
    previous_path = CACHE / "image-plan.json"
    previous = {item["source"]: item for item in json.loads(previous_path.read_text())} if previous_path.exists() else {}

    def process(url: str) -> dict:
        """验证候选图片并计算 Git blob 与内容摘要"""
        if url in previous and previous[url].get("verified"):
            return previous[url]
        candidates = [canonical(url)]
        name = Path(unquote(urlparse(url.replace("\\", "/")).path)).name
        if len(by_name.get(name, [])) == 1:
            candidates.append(RAW + quote(by_name[name][0], safe="/"))
        candidates.extend(canonical(value) for value in alternatives[url])
        for file in (ROOT / "Pics").rglob(name) if name else []:
            if file.is_file():
                data = file.read_bytes()
                try:
                    ext = image_type(data)
                    sha = hashlib.sha256(data).hexdigest()
                    path = CACHE / "upload" / f"{sha}.{ext}"
                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
                    return {"source": url, "sha256": sha, "file": str(path.relative_to(ROOT)),
                            "target": RAW + f"picgo/{sha}.{ext}", "status": "upload", "verified": False}
                except ValueError:
                    pass
        errors = []
        for candidate in dict.fromkeys(candidates):
            try:
                data, ext = download(candidate)
                sha256 = hashlib.sha256(data).hexdigest()
                blob_sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
                if candidate.startswith(RAW):
                    target = candidate
                elif blob_sha in by_sha:
                    target = RAW + quote(by_sha[blob_sha], safe="/")
                    check, _ = download(target)
                    if check != data:
                        raise ValueError("复用图床图片的内容不一致")
                else:
                    path = CACHE / "upload" / f"{sha256}.{ext}"
                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
                    return {"source": url, "resolved": candidate, "sha256": sha256,
                            "file": str(path.relative_to(ROOT)), "target": RAW + f"picgo/{sha256}.{ext}",
                            "status": "upload", "verified": False}
                return {"source": url, "resolved": candidate, "sha256": sha256,
                        "target": target, "status": "reuse", "verified": True}
            except (requests.RequestException, ValueError) as exc:
                errors.append(f"{candidate}: {exc}")
        return {"source": url, "status": "unresolved", "verified": False, "errors": errors}

    plan = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for item in pool.map(process, urls):
            plan.append(item)
            print(item["status"], item["source"], flush=True)
    save_json(previous_path, plan)


def upload() -> None:
    """以一次非强制 Git 提交上传新图片，并逐个验证公开读取的字节"""
    plan_path = CACHE / "image-plan.json"
    plan = json.loads(plan_path.read_text())
    pending = {item["target"]: item for item in plan if item["status"] == "upload"}
    github = GitHub()
    ref = github.api(f"repos/{REPO}/git/ref/heads/master")["object"]["sha"]
    commit = github.api(f"repos/{REPO}/git/commits/{ref}")
    tree = github.tree()
    existing = {item["path"]: item["sha"] for item in tree["tree"]}
    changes = []
    for target, item in pending.items():
        path = unquote(target[len(RAW):])
        data = (ROOT / item["file"]).read_bytes()
        digest = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if path in existing:
            if existing[path] != digest:
                raise ValueError("同名图片内容不一致，拒绝覆盖")
            continue
        blob = github.api(f"repos/{REPO}/git/blobs", {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        changes.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print("已暂存图片", len(changes), "/", len(pending), flush=True)
    if changes:
        tree = github.api(f"repos/{REPO}/git/trees", {"base_tree": commit["tree"]["sha"], "tree": changes})
        new_commit = github.api(f"repos/{REPO}/git/commits", {
            "message": "docs 图床: 归档博客迁移图片", "tree": tree["sha"], "parents": [ref]})
        github.api(f"repos/{REPO}/git/refs/heads/master", {"sha": new_commit["sha"], "force": False}, "PATCH")
        save_json(CACHE / "picture-commit.json", {"sha": new_commit["sha"], "images": len(changes)})
    def verify(item: dict) -> None:
        """并发读取公开图片，按内容校验上传结果"""
        data, _ = download(item["target"])
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError("上传后的图片校验失败")
        item["verified"] = True
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(verify, [item for item in plan if item["status"] == "upload"]))
    save_json(plan_path, plan)


def apply() -> None:
    """仅替换上传后校验成功的图片，未恢复项继续保留原始证据"""
    plan = json.loads((CACHE / "image-plan.json").read_text())
    mapping = {item["source"]: item["target"] for item in plan if item.get("verified")}
    for file in [ROOT / "README.md", *sorted((ROOT / "Docs").glob("*.md"))]:
        def replace(match: re.Match) -> str:
            """保持图片语法、alt 和展示属性，只修改地址"""
            raw = match[1] or match[2]
            if raw is None:
                return match[0]
            for old in sorted(mapping, key=len, reverse=True):
                if raw == old or raw.startswith(old + ' "'):
                    return match[0].replace(old, mapping[old], 1)
            return match[0]
        result = []
        for block in blocks(file.read_text()):
            if re.match(r"^\s*(`{3,}|~{3,})", block):
                result.append(block)
            else:
                # 图片先于行内代码匹配，允许 alt 本身包含反引号
                pattern = re.compile(IMAGE_PATTERN.pattern + r"|(`+[^`\n]*`+)", re.I)
                result.append(pattern.sub(replace, block))
        file.write_text("\n\n".join(result).strip() + "\n")
    save_json(ROOT / "migration" / "images.json", [
        {key: item[key] for key in ["source", "target", "sha256", "status", "verified"] if key in item}
        for item in plan])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "upload", "apply"])
    args = parser.parse_args()
    {"prepare": prepare, "upload": upload, "apply": apply}[args.command]()
