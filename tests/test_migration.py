"""用具有损坏风险的样本验证正文、代码与图片提取"""
import sys
import json
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from archive import html_to_markdown, unwrap_url
from images import image_urls, image_type
from reconcile import blocks, clean_promotion, title_key


class MigrationTests(unittest.TestCase):
    """确保迁移不会把代码、正文与参考文献当作宣传删除"""

    def test_code_and_table(self):
        body = BeautifulSoup('<article><h2>示例</h2><pre><code class="language-html">&lt;template&gt;{{ a }}&lt;/template&gt;\n\n```</code></pre><table><tr><th>字段</th></tr><tr><td>值</td></tr></table></article>', 'html.parser').article
        text = html_to_markdown(body, 'https://example.com')
        self.assertIn('````html\n<template>{{ a }}</template>\n\n```\n````', text)
        self.assertIn('| 字段 |', text)

    def test_promotion_keeps_references(self):
        text = '# 正文\n\n内容\n\n---\n网上的帖子大多深浅不一，欢迎点赞\n\n> 参考文档：\n> 1. [文档](https://example.com)\n\nPS：本人博客地址，欢迎关注我的公众号\n\n![](https://example.com/qr.png)\n'
        result = clean_promotion(text)
        self.assertIn('参考文档', result)
        self.assertIn('内容', result)
        self.assertNotIn('公众号', result)
        self.assertNotIn('qr.png', result)

    def test_code_images_untouched(self):
        text = '```md\n![](https://example.com/code.png)\n\n```\n\n![正文](https://example.com/body.gif)'
        self.assertEqual(image_urls(text), ['https://example.com/body.gif'])
        self.assertEqual(len(blocks(text)), 2)
        self.assertEqual(image_urls('示例 `<img src="https://example.com/unsafe">`'), [])

    def test_redirect_and_identity(self):
        self.assertEqual(unwrap_url('https://link.juejin.cn/?target=https%3A%2F%2Fexample.com%2Fa%23b'), 'https://example.com/a#b')
        self.assertEqual(title_key('我的 2018 年终总结 | 掘金年度征文'), title_key('2018 年终总结'))
        with self.assertRaises(ValueError):
            image_type('<html>访问限制</html>'.encode())

    def test_delivered_images(self):
        root = Path(__file__).resolve().parents[1]
        missing = {item['source'] for item in json.loads((root / '.vitepress/data/missing-images.json').read_text())}
        mapping_path = root / 'migration/images.json'
        mapping = json.loads(mapping_path.read_text()) if mapping_path.exists() else None
        verified = {item['target'] for item in mapping if item.get('verified')} if mapping is not None else None
        unresolved = set()
        for file in [root / 'README.md', *(root / 'Docs').glob('*.md')]:
            for source in image_urls(file.read_text()):
                if source in missing:
                    unresolved.add(source)
                else:
                    if verified is not None:
                        self.assertTrue(source in verified, f'{file.name}: {source}')
                    self.assertTrue(source.startswith('https://raw.githubusercontent.com/SHERlocked93/pic/master/'))
        self.assertEqual(unresolved, missing)

    def test_local_archive_identity(self):
        """来源映射只保留本地；存在归档记录时核验分页总数和唯一性"""
        root = Path(__file__).resolve().parents[1]
        path = root / 'migration/articles.json'
        if not path.exists():
            self.skipTest('本机未保存平台来源归档，站点不依赖该记录')
        articles = json.loads(path.read_text())['articles']
        keys = [(source['platform'], source['id']) for article in articles for source in article['sources']]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(sum(platform == 'segmentfault' for platform, _ in keys), 114)
        self.assertEqual(sum(platform == 'juejin' for platform, _ in keys), 75)


if __name__ == '__main__':
    unittest.main()
