#!/usr/bin/env python3
"""
作用：为平台正文和本地文章生成匹配清单与差异报告
Usage: python scripts/reconcile.py
Options: 无参数
Description: 读取 archive.py 的缓存与 Docs；只写缓存候选，不覆盖原文
"""

from __future__ import annotations

import difflib
import json
import re
import unicodedata
from pathlib import Path

from archive import CACHE, ROOT, save_json


def title_key(title: str) -> str:
    """忽略标题排版差异，同时保留具有区分意义的主题词"""
    title = unicodedata.normalize("NFKC", title).lower()
    title = re.sub(r"sherlocked93\s*的?", "", title)
    if re.search(r"20\d{2}.*年终总结", title):
        return re.search(r"20\d{2}", title)[0] + "年终总结"
    if "chrome 87" in title:
        return "chrome87新特性"
    title = re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", title)
    title = title.replace("手摸手设计模式系列", "javascript设计模式系列")
    aliases = {
        "c中的编译和链接": "c的编译与链接",
        "c的vs项目中引入跨平台包管理工具conan": "c跨平台包管理工具conan",
        "c的vs项目引入公共配置文件": "c中vs项目中引入公共配置文件",
        "把时间当作朋友李笑来阅读摘要": "把时间当作朋友阅读摘要",
        "mac上clion搭建qt66开发环境": "mac上使用clion开发qt6配置",
        "掌控情绪成为自己的主宰蛤蟆先生去看心理医生": "掌控情绪做人生的主人",
        "这些js中强大的操作符总有几个你没听说过": "这些js中的操作符总有几个你没听说过",
        "chrome89新功能一览性能提升明显大量devtools新特性": "chrome89新功能一览大量devtools新特性",
        "我最近在看什么富爸爸穷爸爸": "富爸爸穷爸爸阅读摘要",
        "打造舒适搬砖环境这些是我最想推介的桌面好物": "生命在于折腾这些桌面好物提升你的搬砖幸福度",
        "centos安装部署yapi": "centos7安装部署yapi",
        "半小时搞会centos入门必备基础知识": "centos基础知识",
        "http2基础教程阅读摘要": "http2基础教程读书笔记",
        "图解http阅读摘要": "图解http读书笔记",
        "git学习笔记": "git笔记",
        "vue项目骨架屏注入实践": "骨架屏实践",
        "js中的offsetscrollclient总结": "js中的offsetscrollclient",
        "vue源码阅读批量异步更新与nexttick原理": "vue源码阅读批量异步更新与nexttick",
        "使用jenkins持续集成前端项目并自动化部署到nginx服务器": "使用jenkins持续集成前端项目并自动化部署到tomcatnginx服务器",
        "javascript函数式编程技巧反柯里化": "js中的反柯里化",
        "javascript函数式编程技巧柯里化": "js中的柯里化",
        "浏览器中的垃圾回收与内存泄漏": "js中的垃圾回收与内存泄漏",
        "css中重要的层叠概念": "css中的层叠和块级格式化上下文",
        "css中重要的bfc": "css中的层叠和块级格式化上下文",
    }
    return aliases.get(title, title)


def clean_promotion(text: str) -> str:
    """只移除完整宣传段落和目录占位符，保留正文与参考文献"""
    text = re.sub(r"(?m)^---\s*\n(?=网上的帖子)", "---\n\n", text)
    paragraphs = re.split(r"\n\s*\n", text)
    result = []
    promotional_tail = False
    for paragraph in paragraphs:
        plain = paragraph.strip()
        if promotional_tail and (re.fullmatch(r"(?:>\s*)?!\[[^\]]*\]\([^\n]+\)", plain)
                                 or re.match(r">?\s*\d+\. \[", plain)):
            continue
        promotional_tail = False
        if re.fullmatch(r"\[TOC\]", plain, re.I):
            continue
        if re.match(r"(?:PS[：:]\s*)?(?:本文|文章)?同步更新于", plain):
            promotional_tail = True
            continue
        if re.match(r"网上的帖子大多深浅不一", plain):
            continue
        if re.match(r"如果发现错误，欢迎留言指出.*点赞", plain):
            continue
        if re.search(r"(?:关注我的公众号|关注文末二维码)", plain):
            promotional_tail = True
            continue
        if plain.startswith("> [掘金翻译计划]"):
            continue
        if re.search(r"(?:欢迎大家|欢迎|更多内容|直接搜索).{0,40}(?:关注|公众号|公众hao|加群)", plain):
            promotional_tail = True
            continue
        if re.match(r"系列文章中，?欢迎", plain):
            promotional_tail = True
            continue
        if re.search(r"前端下午茶交流(?:群|qun)", plain) or "微信搜索 `qianyu" in plain:
            promotional_tail = True
            continue
        if re.search(r"本文参与了.*(?:征文|活动)", plain):
            continue
        if "作者其他高赞文章" in plain:
            promotional_tail = True
            continue
        if re.search(r"(?:扫码|扫描二维码).{0,20}(?:关注|加群)", plain):
            promotional_tail = True
            continue
        if re.search(r"(?:PS[：:]|本人博客地址).*公众号", plain):
            promotional_tail = True
            continue
        result.append(paragraph)
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(result)).strip() + "\n"


def normalize(text: str) -> str:
    """以文字和代码内容比较正文，不把链接地址及排版变化视作内容扩充"""
    text = clean_promotion(text)
    text = re.sub(r"!\[[^\]]*\]\([^\n]*?\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", text)


def shingles(text: str) -> set[str]:
    """取较长文本片段衡量完整内容的覆盖率"""
    value = normalize(text)
    return {value[i:i + 12] for i in range(max(1, len(value) - 11))}


def coverage(first: str, second: str) -> float:
    """计算前一正文的内容有多少可在后一正文中找到"""
    a, b = shingles(first), shingles(second)
    return len(a & b) / max(1, len(a))


def blocks(text: str) -> list[str]:
    """将围栏代码作为整体保留，避免在代码内的空行处插入正文"""
    output, paragraph, fence = [], [], None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker and fence is None:
            if paragraph:
                output.append("\n".join(paragraph)); paragraph = []
            fence = marker[1]
            paragraph.append(line)
        elif fence is not None:
            paragraph.append(line)
            if re.fullmatch(r"\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                output.append("\n".join(paragraph)); paragraph = []; fence = None
        elif not line.strip():
            if paragraph:
                output.append("\n".join(paragraph)); paragraph = []
        else:
            paragraph.append(line)
    if paragraph:
        output.append("\n".join(paragraph))
    return output


def propose(group: dict) -> tuple[str, list[dict]]:
    """仅把能定位到原有段落附近的明显新增内容列为合并候选"""
    sources = group["sources"]
    if not group["local"]:
        primary = max(sources, key=lambda x: len(normalize(x["markdown"])))
        return clean_promotion(primary["markdown"]), []
    base = blocks(clean_promotion(group["local"]))
    base_keys = [normalize(block) for block in base]
    base_shingles = shingles("\n\n".join(base))
    additions = []
    for source in sources:
        remote = blocks(clean_promotion(source["markdown"]))
        anchor = None
        for block in remote:
            key = normalize(block)
            matches = [i for i, old_key in enumerate(base_keys) if key and key == old_key]
            if matches:
                anchor = matches[0]
                continue
            block_shingles = shingles(block)
            if block.startswith("#") or len(key) < 35 or len(block_shingles & base_shingles) / max(1, len(block_shingles)) >= .72:
                continue
            # 改写段落与现有段落近似时保留本地，交给逐篇差异核对
            similarity = max((difflib.SequenceMatcher(None, key, old_key, autojunk=True).ratio()
                              for old_key in base_keys if abs(len(old_key) - len(key)) < len(key)), default=0)
            if similarity > .68 or anchor is None:
                continue
            anchor += 1
            base.insert(anchor, block)
            base_keys.insert(anchor, key)
            base_shingles.update(block_shingles)
            additions.append({"source": source["url"], "text": block})
    return "\n\n".join(base).strip() + "\n", additions


def reconcile() -> None:
    """建立明确匹配；复杂差异生成可供人工逐篇核对的报告"""
    groups, lookup = [], {}
    for file in sorted((ROOT / "Docs").glob("*.md")):
        text = file.read_text()
        match = re.search(r"^#\s+(.+)", text, re.M)
        title = match[1].strip() if match else file.stem
        group = {"file": str(file.relative_to(ROOT)), "title": title, "local": text, "sources": []}
        groups.append(group)
        for name in [file.stem, title]:
            lookup[title_key(name)] = group
    fetched = json.loads((CACHE / "fetched.json").read_text())
    for source in fetched:
        if source["status"] != "fetched":
            continue
        key = title_key(source["title"])
        if key not in lookup:
            name = re.sub(r'[<>:"/\\|?*]', "", source["title"]).strip()
            lookup[key] = {"file": f"Docs/{name}.md", "title": source["title"], "local": "", "sources": []}
            groups.append(lookup[key])
        lookup[key]["sources"].append(source)
    report = []
    for index, group in enumerate(groups):
        local = group["local"]
        comparisons = []
        for source in group["sources"]:
            remote = source["markdown"]
            comparisons.append({"source": source["url"], "title": source["title"], "chars": len(remote),
                "local_in_remote": round(coverage(local, remote), 4) if local else None,
                "remote_in_local": round(coverage(remote, local), 4) if local else None})
            diff = "\n".join(difflib.unified_diff(clean_promotion(local).splitlines(),
                clean_promotion(remote).splitlines(), fromfile=group["file"], tofile=source["url"], lineterm=""))
            path = CACHE / "diffs" / f"{index}-{source['platform']}.diff"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(diff)
        report.append({"file": group["file"], "title": group["title"], "local_chars": len(local),
                       "comparisons": comparisons})
        candidate, additions = propose(group)
        target = CACHE / "candidates" / Path(group["file"]).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(candidate)
        group["additions"] = additions
    save_json(CACHE / "groups.json", groups)
    save_json(CACHE / "comparison.json", report)
    print("本地", sum(bool(x["local"]) for x in groups), "新增候选", sum(not x["local"] for x in groups))


if __name__ == "__main__":
    reconcile()
