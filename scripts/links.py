#!/usr/bin/env python3
"""
作用：将本人文章链接统一到 GitHub Markdown，保留第三方资料和代码示例
Usage: python scripts/links.py resolve|apply
Options: resolve 解析平台跳转和旧地址；apply 仅应用已经确认的文章映射
Description: 读取 migration/articles.json；resolve 联网读取跳转目标并缓存
             apply 修改 Docs 和 README；未能解析的链接写入忽略目录供人工核对
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
from urllib.parse import quote, unquote, urlparse

import requests
from bs4 import BeautifulSoup

from archive import CACHE, ROOT, save_json, unwrap_url
from reconcile import blocks, title_key

# 非代码段落中的 URL；Markdown 的括号与引号是地址边界
URL = re.compile(r'https?://[^\s<>"\')\]]+')
INLINE = re.compile(r'(`+)([^`]|(?!(?<!`)\1)`)*?\1')


def github_url(file: str) -> str:
    """生成本人文章的 GitHub Markdown 地址"""
    return "https://github.com/SHERlocked93/blog/blob/master/" + quote(file, safe="/")


def editable_parts(block: str) -> list[str]:
    """划分行内代码，代码内容保持原样"""
    return re.split(r"(`+[^`\n]*`+)", block)


def resolve() -> None:
    """解析遗留掘金地址与平台包装，不将重定向页面当作文章"""
    articles = json.loads((ROOT / "migration/articles.json").read_text())["articles"]
    known = {source["id"] for article in articles for source in article["sources"]}
    files = [ROOT / "README.md", *sorted((ROOT / "Docs").glob("*.md"))]
    urls = set()
    for file in files:
        for block in blocks(file.read_text()):
            if block.startswith(("```", "~~~")):
                continue
            for part in editable_parts(block)[::2]:
                for url in URL.findall(part):
                    if "link.segmentfault.com/" in url or "link.juejin.cn/" in url or re.search(r"juejin\.(?:im|cn)/post/[0-9a-f]{24}(?:$|[?#])", url):
                        urls.add(url)
    path = CACHE / "redirects.json"
    resolved = json.loads(path.read_text()) if path.exists() else {}

    def run(url: str) -> tuple[str, dict]:
        """读取 HTTP 跳转或页面中明确提供的目标，不猜测 URL"""
        if url in resolved and resolved[url].get("target"):
            return url, resolved[url]
        unwrapped = unwrap_url(url)
        if unwrapped != url:
            return url, {"target": unwrapped}
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            response.raise_for_status()
            target = response.url
            if urlparse(target).netloc.startswith("link."):
                soup = BeautifulSoup(response.text, "html.parser")
                for node in soup.select('a[href^="http"]'):
                    value = node["href"]
                    if not urlparse(value).netloc.endswith(("segmentfault.com", "juejin.cn")):
                        target = value
                        break
                for pattern in [r'(?:location\.href|location\.replace)\s*[=(]\s*["\']([^"\']+)',
                                r'URL=["\']?(https?://[^"\'<>]+)']:
                    match = re.search(pattern, response.text, re.I)
                    if match:
                        target = match[1]; break
            if target == url and not urlparse(target).path.startswith("/post/"):
                return url, {"error": "页面未提供可验证的目标"}
            return url, {"target": target}
        except requests.RequestException as exc:
            return url, {"error": str(exc)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for source, result in pool.map(run, sorted(urls)):
            resolved[source] = result
            print("resolved" if result.get("target") else "unresolved", source[:120], flush=True)
    save_json(path, resolved)


def recover_parallel_links() -> None:
    """用同篇文章其他版本的明确链接还原平台包装，不猜测无法辨认的链接"""
    from collections import defaultdict
    groups = json.loads((CACHE / "groups.json").read_text())
    path = CACHE / "redirects.json"
    redirects = json.loads(path.read_text()) if path.exists() else {}
    pattern = re.compile(r'\[([^\]\n]+)\]\((https?://[^\s)]+)')
    global_targets = defaultdict(set)
    for group in groups:
        for text in [group["local"], *(s["markdown"] for s in group["sources"])]:
            for label, url in pattern.findall(text):
                if not urlparse(url).netloc.startswith("link."):
                    global_targets[label.strip()].add(url)
    count = 0
    for group in groups:
        targets, wrapped = defaultdict(set), []
        for text in [group["local"], *(s["markdown"] for s in group["sources"])]:
            for label, url in pattern.findall(text):
                if urlparse(url).netloc.startswith("link."):
                    wrapped.append((label.strip(), url))
                else:
                    targets[label.strip()].add(url)
        for label, url in wrapped:
            candidates = targets[label] or (global_targets[label] if len(label) > 8 else set())
            if label.startswith(("https://", "http://")) and not any(char.isspace() for char in label):
                candidates = {label}
            if len(candidates) == 1 and not redirects.get(url, {}).get("target"):
                redirects[url] = {"target": next(iter(candidates)), "evidence": "同名引用在平行正文版本中的明确地址"}
                count += 1
    save_json(path, redirects)
    print("从平行版本恢复链接", count)


def apply() -> None:
    """根据已核对的文章身份替换文章 URL，章节锚点转换为 GitHub 标题形式"""
    articles = json.loads((ROOT / "migration/articles.json").read_text())["articles"]
    id_map = {source["id"]: article for article in articles for source in article["sources"]}
    by_title = {title_key(article["title"]): article for article in articles}
    redirects_path = CACHE / "redirects.json"
    redirects = json.loads(redirects_path.read_text()) if redirects_path.exists() else {}
    aliases = {}
    # README 中的旧掘金 ID 通过已核实的标题建立别名，避免依赖已失效的旧域名
    original = __import__("subprocess").run(["git", "show", "HEAD:README.md"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", original):
        match = re.search(r"juejin\.(?:im|cn)/post/([0-9a-f]{24})", url)
        key = title_key(label.replace("\\", ""))
        if match and key in by_title:
            aliases[match[1]] = by_title[key]
    mapping_path = ROOT / "migration" / "links.json"
    replacements = json.loads(mapping_path.read_text()) if mapping_path.exists() else {}
    unresolved = []

    def rewrite(url: str, file: str) -> str:
        """只将已识别的本人文章变更为文件链接"""
        target = redirects.get(url, {}).get("target") or unwrap_url(url)
        parsed = urlparse(target)
        match = re.search(r"(?:segmentfault\.com/a/|juejin\.(?:im|cn)/(?:post|entry)/)([0-9a-f]+)", target)
        article = (id_map.get(match[1]) or aliases.get(match[1])) if match else None
        if parsed.netloc.lower() == "github.com" and parsed.path.lower().startswith("/sherlocked93/blog/"):
            for candidate in articles:
                if unquote(parsed.path).endswith("/" + candidate["file"]):
                    article = candidate; break
        if article:
            result = github_url(article["file"])
            if parsed.fragment:
                fragment = unquote(parsed.fragment)
                if re.fullmatch(r"heading-\d+", fragment):
                    source = next((s for s in article["sources"] if s["url"].split("#")[0] == target.split("#")[0]), None)
                    if source:
                        cache = CACHE / "articles" / f"{source['platform']}-{source['id']}.json"
                        value = json.loads(cache.read_text())["markdown"]
                        headings = [block.splitlines()[0].lstrip("# ") for block in blocks(value)
                                    if re.match(r"^#{2,6} ", block)]
                        index = int(fragment.split("-")[1])
                        if index < len(headings):
                            fragment = headings[index]
                fragment = re.sub(r"[^\w\-\s\u4e00-\u9fff]", "", fragment.lower()).replace(" ", "-")
                result += "#" + quote(fragment)
            if url != result:
                replacements[url] = result
            return result
        if match and match[1] not in id_map and match[1] not in aliases:
            unresolved.append({"file": file, "url": url})
        return target

    for file in [ROOT / "README.md", *sorted((ROOT / "Docs").glob("*.md"))]:
        output = []
        for block in blocks(file.read_text()):
            if re.match(r"^\s*(`{3,}|~{3,})", block):
                output.append(block); continue
            parts = editable_parts(block)
            for index in range(0, len(parts), 2):
                parts[index] = URL.sub(lambda match: rewrite(match[0], str(file.relative_to(ROOT))), parts[index])
            output.append("".join(parts))
        file.write_text("\n\n".join(output).strip() + "\n")
    save_json(CACHE / "unmapped-links.json", unresolved)
    save_json(ROOT / "migration" / "links.json", replacements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["resolve", "recover", "apply"])
    args = parser.parse_args()
    {"resolve": resolve, "recover": recover_parallel_links, "apply": apply}[args.command]()
