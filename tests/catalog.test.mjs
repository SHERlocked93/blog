import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, existsSync } from 'node:fs'
import MarkdownIt from 'markdown-it'

// 直接检查交付内容，避免元数据和实际正文或导航脱节
const catalog = JSON.parse(readFileSync(new URL('../.vitepress/data/articles.json', import.meta.url), 'utf8'))
const parser = new MarkdownIt({ html: true })

test('每个文章文件唯一存在，分类必须已登记', () => {
  const files = new Set()
  for (const article of catalog.articles) {
    assert.ok(!files.has(article.file), article.file)
    assert.ok(existsSync(new URL('../' + article.file, import.meta.url)), article.file)
    files.add(article.file)
    assert.ok(catalog.categories.includes(article.category), article.file)
  }
})

test('站点索引覆盖可见文章，排除推广专题', () => {
  const content = readFileSync(new URL('../articles.md', import.meta.url), 'utf8')
  const links = []
  for (const token of parser.parse(content, {})) {
    for (const child of token.children || []) {
      if (child.type === 'link_open') links.push(decodeURI(child.attrGet('href')))
    }
  }
  for (const article of catalog.articles) {
    const route = '/' + article.file.replace(/\.md$/, '.html')
    assert.equal(links.includes(route), !article.excluded, article.file)
  }
})

test('README 的文章目录只使用 GitHub Markdown 地址', () => {
  const content = readFileSync(new URL('../README.md', import.meta.url), 'utf8').split('## 博客')[1].split('## 已读书单')[0]
  const links = []
  for (const token of parser.parse(content, {})) {
    for (const child of token.children || []) {
      if (child.type === 'link_open') links.push(child.attrGet('href'))
    }
  }
  assert.equal(links.filter(link => link.startsWith('https://github.com/SHERlocked93/blog/blob/master/Docs/')).length,
    catalog.articles.filter(article => !article.excluded).length)
})

test('正文中的 GitHub 文章链接指向已收录文件，代码示例不参与链接校验', () => {
  const files = new Set(catalog.articles.map(article => article.file))
  for (const article of catalog.articles) {
    const tokens = parser.parse(readFileSync(new URL('../' + article.file, import.meta.url), 'utf8'), {})
    for (const token of tokens) {
      for (const child of token.children || []) {
        if (child.type !== 'link_open') continue
        const href = child.attrGet('href') || ''
        const file = href.match(/^https:\/\/github\.com\/SHERlocked93\/blog\/blob\/master\/(Docs\/[^#?]+)/i)?.[1]
        if (file) {
          assert.ok(files.has(decodeURIComponent(file)), `${article.file}: ${href}`)
          assert.ok(existsSync(new URL('../' + file, import.meta.url)), `${article.file}: ${href}`)
        }
      }
    }
  }
})
