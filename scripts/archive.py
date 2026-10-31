#!/usr/bin/env python3
"""
作用：归档本人公开文章，保留可核对的来源与正文候选
Usage: python scripts/archive.py discover|fetch
Options: discover 获取平台目录；fetch 获取目录中的完整正文；--refresh 忽略请求缓存
Description: 需先安装 scripts/requirements.txt 中的依赖；联网读取公开页面
             目录与正文写入被 Git 忽略的 .migration-cache，不直接覆盖 Docs
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import MarkdownConverter

# 仓库根目录和请求缓存，缓存不参与博客发布
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".migration-cache"
SF_AUTHOR = 1030000007673508
JJ_AUTHOR = "360295543341165"


def save_json(path: Path, value: Any) -> None:
    """保存可读的 UTF-8 清单"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def request(url: str, payload: dict | None = None, refresh: bool = False) -> str:
    """缓存公开请求，拒绝把错误页面当作正文"""
    key = hashlib.sha256((url + json.dumps(payload, sort_keys=True)).encode()).hexdigest()
    path = CACHE / "http" / f"{key}.txt"
    if path.exists() and not refresh:
        return path.read_text()
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://juejin.cn/"}
    error = None
    for attempt in range(3):
        try:
            response = requests.request("POST" if payload is not None else "GET", url,
                                        json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"
            text = response.text
            if "segmentfault.com" in url and "__NEXT_DATA__" not in text:
                raise ValueError("思否响应缺少页面数据")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            return text
        except (requests.RequestException, ValueError) as exc:
            error = exc
            time.sleep(attempt + 1)
    raise RuntimeError(f"{url}: {error}")


def next_state(html: str) -> dict:
    """读取思否服务端输出的 JSON 状态，不执行网页脚本"""
    soup = BeautifulSoup(html, "html.parser")
    node = soup.find("script", id="__NEXT_DATA__")
    if node is None:
        raise ValueError("缺少 __NEXT_DATA__")
    return json.loads(node.string)["props"]["pageProps"]["initialState"]


def unwrap_url(url: str, base: str = "") -> str:
    """还原平台跳转包装，保留真实目标及锚点"""
    url = urljoin(base, url)
    for _ in range(3):
        parsed = urlparse(url)
        if parsed.netloc in {"link.juejin.cn", "link.segmentfault.com"}:
            query = parse_qs(parsed.query)
            target = (query.get("target") or query.get("url") or [None])[0]
            if target:
                url = target
                continue
        break
    return url


def discover(refresh: bool = False) -> None:
    """枚举掘金游标与思否专栏分页，保存交叉核对用的原始目录"""
    articles: dict[str, dict] = {}
    cursor, seen = "0", set()
    jj_count = None
    while cursor not in seen:
        seen.add(cursor)
        value = json.loads(request("https://api.juejin.cn/content_api/v1/article/query_list", {
            "user_id": JJ_AUTHOR, "sort_type": 2, "cursor": cursor, "limit": 20,
        }, refresh))
        if value.get("err_no") != 0:
            raise ValueError(value.get("err_msg"))
        jj_count = value.get("count")
        for row in value["data"]:
            item = row["article_info"]
            if str(item["user_id"]) != JJ_AUTHOR:
                raise ValueError("掘金作者身份不匹配")
            article_id = str(item["article_id"])
            articles["jj:" + article_id] = {
                "platform": "juejin", "id": article_id, "title": item["title"],
                "url": f"https://juejin.cn/post/{article_id}",
                "created": item.get("ctime"), "modified": item.get("mtime"),
            }
        print("掘金目录", len(articles), "总数", jj_count, flush=True)
        if not value.get("has_more"):
            break
        cursor = value["cursor"]
    jj_actual = len(articles)
    if jj_actual != jj_count:
        raise ValueError(f"掘金目录数量不一致：{jj_actual}/{jj_count}")

    # 作者页受访问限制时，用公开专栏和仓库已引用的文章补充枚举
    sf_total_pages, page, sf_rows = 1, 1, set()
    while page <= sf_total_pages:
        url = "https://segmentfault.com/blog/sherlocked93" + (f"?page={page}" if page > 1 else "")
        data = next_state(request(url, refresh=refresh))["blogHome"]["articleData"]
        sf_total_pages = data["total_page"]
        for row in data["rows"]:
            item = row.get("article", row)
            article_id = str(item["id"])
            sf_rows.add(article_id)
            articles["sf:" + article_id] = {
                "platform": "segmentfault", "id": article_id, "title": item["title"],
                "url": f"https://segmentfault.com/a/{article_id}",
                "created": item.get("created"), "modified": item.get("modified"),
            }
        print("思否专栏", page, "/", sf_total_pages, "累计", len(sf_rows), flush=True)
        page += 1
    # 作者目录存在不含 Next 状态的服务端 HTML，单独按可见文章链接和分页解析
    sample = json.loads(re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>',
        request("https://segmentfault.com/a/1190000044634219"), re.S)[1])
    build_id = sample["buildId"]
    author_rows, author_total, page, last_page = set(), None, 1, 1
    while page <= last_page:
        path = CACHE / f"author-{page}.html"
        if path.exists() and not refresh:
            html = path.read_text()
        else:
            url = f"https://segmentfault.com/_next/data/{build_id}/u/sherlocked93/articles.json?sort=newest&page={page}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"
            html = response.text
            if "SHERlocked93 的文章" not in html:
                raise ValueError("思否作者目录未返回正确页面")
            path.write_text(html)
        soup = BeautifulSoup(html, "html.parser")
        description = soup.find("meta", attrs={"name": "description"})
        count = re.search(r"有\s*(\d+)\s*篇文章", description.get("content", ""))
        if count:
            author_total = int(count[1])
        for node in soup.select('a[href^="/a/"]'):
            match = re.fullmatch(r"/a/(\d+)", node["href"])
            if match:
                article_id = match[1]
                author_rows.add(article_id)
                articles.setdefault("sf:" + article_id, {"platform": "segmentfault", "id": article_id,
                    "title": node.get_text(strip=True), "url": f"https://segmentfault.com/a/{article_id}"})
        pages = [int(parse_qs(urlparse(node["href"]).query).get("page", [1])[0])
                 for node in soup.select(".pagination a[href]")]
        last_page = max([last_page, *pages])
        print("思否作者", page, "/", last_page, "累计", len(author_rows), "总数", author_total, flush=True)
        page += 1
    if len(author_rows) != author_total:
        raise ValueError(f"思否作者目录不完整：{len(author_rows)}/{author_total}")
    texts = [ROOT / "README.md", *sorted((ROOT / "Docs").glob("*.md"))]
    for file in texts:
        for article_id in re.findall(r"segmentfault\.com/a/(\d+)", unquote(file.read_text())):
            articles.setdefault("sf:" + article_id, {
                "platform": "segmentfault", "id": article_id, "title": "",
                "url": f"https://segmentfault.com/a/{article_id}",
            })
    save_json(CACHE / "sources.json", list(articles.values()))
    save_json(CACHE / "discovery.json", {"juejin_count": jj_count, "juejin_enumerated": jj_actual,
        "segmentfault_blog_pages": sf_total_pages, "segmentfault_blog_enumerated": len(sf_rows),
        "segmentfault_author_enumerated": len(author_rows), "segmentfault_author_count": author_total})


def code_language(node: Tag) -> str:
    """从平台的 pre/code 标签还原代码语言"""
    for tag in [node, node.find("code")]:
        if tag is None:
            continue
        for name in tag.get("class", []):
            if name.startswith(("language-", "lang-")):
                return name.split("-", 1)[1]
    return "text"


class ArticleConverter(MarkdownConverter):
    """保存代码内容，避免示例 HTML 被误当作可运行组件"""

    def convert_pre(self, el: Tag, text: str, parent_tags: set) -> str:
        """以原始文本生成长度足够的代码围栏"""
        value = el.get_text().strip("\n")
        runs = re.findall(r"`+", value)
        fence = "`" * max(3, max(map(len, runs), default=0) + 1)
        return f"\n\n{fence}{code_language(el)}\n{value}\n{fence}\n\n"


def html_to_markdown(body: Tag, base: str) -> str:
    """转换正文并恢复懒加载图片与原始链接"""
    for node in body.select("style, script, .copy-code-btn, .code-block-extension-header"):
        node.decompose()
    for node in body.select("img"):
        for key in ["data-src", "data-original", "src"]:
            if node.get(key) and not node[key].startswith("data:"):
                node["src"] = urljoin(base, node[key])
                break
    for node in body.select("a[href]"):
        node["href"] = unwrap_url(node["href"], base)
    return ArticleConverter(heading_style="ATX", bullets="-", escape_underscores=False,
                            escape_asterisks=False).convert(str(body)).strip() + "\n"


def fetch_article(source: dict, refresh: bool = False) -> dict:
    """提取单篇完整正文并验证归属，不把失败响应写入文章"""
    key = source["platform"] + "-" + source["id"]
    output = CACHE / "articles" / (key + ".json")
    if output.exists() and not refresh:
        return json.loads(output.read_text())
    html = request(source["url"], refresh=refresh)
    soup = BeautifulSoup(html, "html.parser")
    if source["platform"] == "segmentfault":
        item = next_state(html)["articleDetail"]["artDetail"][source["id"]]["article"]
        if item["user_id"] != SF_AUTHOR:
            return {**source, "status": "third_party"}
        title = item["title"]
        body = soup.select_one("article.article")
        source = {**source, "created": item.get("created"), "modified": item.get("modified"),
                  "author_article_count": item["user"].get("articles")}
    else:
        body = soup.select_one('[itemprop="articleBody"] .article-viewer')
        title_node = soup.select_one("h1.article-title") or soup.select_one("h1")
        title = title_node.get_text(strip=True) if title_node else source["title"]
        # 归属由带 user_id 的作者目录提供；正文页必须有对应文章地址
        if not soup.select_one('[itemprop="articleBody"]'):
            raise ValueError("掘金未返回正文，可能为访问校验页")
    if body is None or len(body.get_text(strip=True)) < 80:
        raise ValueError("完整正文缺失或过短")
    text = html_to_markdown(body, source["url"])
    result = {**source, "title": title, "markdown": f"# {title}\n\n{text}",
              "status": "fetched", "headings": len(body.select("h1,h2,h3,h4,h5,h6"))}
    save_json(output, result)
    return result


def fetch_all(refresh: bool = False) -> None:
    """有界并发抓取正文，保留失败项并补充作者自己的互链文章"""
    sources = json.loads((CACHE / "sources.json").read_text())
    results, processed = [], set()
    while sources:
        def run(source: dict) -> dict:
            """将单篇访问错误留作可重试记录"""
            try:
                return fetch_article(source, refresh)
            except (requests.RequestException, RuntimeError, ValueError, KeyError) as exc:
                return {**source, "status": "failed", "error": str(exc)}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            for result in pool.map(run, sources):
                results.append(result)
                processed.add((result["platform"], result["id"]))
                print(result["status"], result["platform"], result["id"], result["title"], flush=True)
        pending = {}
        for result in results:
            if result["status"] != "fetched":
                continue
            for article_id in re.findall(r"segmentfault\.com/a/(\d+)", result["markdown"]):
                if ("segmentfault", article_id) not in processed:
                    pending[article_id] = {"platform": "segmentfault", "id": article_id,
                        "url": f"https://segmentfault.com/a/{article_id}", "title": ""}
        sources = list(pending.values())
    save_json(CACHE / "fetched.json", results)


def main() -> None:
    """执行只生成候选的抓取步骤"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["discover", "fetch"])
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if args.command == "discover":
        discover(args.refresh)
    else:
        fetch_all(args.refresh)


if __name__ == "__main__":
    main()
