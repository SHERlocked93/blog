#!/usr/bin/env node
/**
 * 作用：从文章清单生成站点分类索引与 README 博客目录
 * Usage: node scripts/catalog.mjs
 * Options: 无参数
 * Description: 维护文章时更新 .vitepress/data/articles.json 后运行，保留 README 的作品和书单
 */
import { readFileSync, writeFileSync } from 'node:fs'

// 文章元数据是导航与目录的共同来源
const catalog = JSON.parse(readFileSync(new URL('../.vitepress/data/articles.json', import.meta.url), 'utf8'))
const articles = catalog.articles.filter(article => !article.excluded)
const order = ['年终总结', 'C/CPP & QT', 'Vue 实践', '源码阅读', 'JavaScript', 'CSS', '浏览器',
  'Nginx', 'Docker', '数据库', 'Node', 'Webpack', '周边技术栈', 'Linux', 'JavaScript 设计模式',
  '翻译', '阅读摘要', '那些好用的工具']

// 页面 URL 与 GitHub Markdown 的用途不同，分别生成
const github = article => `https://github.com/SHERlocked93/blog/blob/master/${encodeURI(article.file).replaceAll('[', '%5B').replaceAll(']', '%5D')}`
const page = article => `/${encodeURI(article.file.replace(/\.md$/, '.html')).replaceAll('[', '%5B').replaceAll(']', '%5D')}`
const label = title => title.replaceAll('[', '\\[').replaceAll(']', '\\]')
const categories = order.filter(category => articles.some(article => article.category === category))
const groups = categories.map(category => ({ category, articles: articles.filter(article => article.category === category)
  .sort((left, right) => Number(right.created || 0) - Number(left.created || 0)
    || left.title.localeCompare(right.title, 'zh-CN')) }))
const sourcePath = new URL('../README.md', import.meta.url)
let readme = readFileSync(sourcePath, 'utf8')
const start = readme.indexOf('## 博客')
const end = readme.indexOf('## 已读书单')
if (start < 0 || end < 0 || start >= end) throw new Error('README 博客目录边界缺失')
const contents = ['## 博客', '', '[在线阅读](https://sherlocked93.github.io/blog/) · 以下文章链接在 GitHub 中打开。', '',
  ...groups.flatMap(group => [`### ${group.category}`, '',
    ...group.articles.map((article, index) => `${index + 1}. [${label(article.title)}](${github(article)})`), '']),
  '---', ''].join('\n')
readme = readme.slice(0, start) + contents + '\n' + readme.slice(end)
writeFileSync(sourcePath, readme)
const technical = new Set(['年终总结', '阅读摘要', '那些好用的工具'])
const section = (title, filter) => [`## ${title}`, '', ...groups.filter(group => filter(group.category)).flatMap(group => [
  `### ${group.category}`, '', ...group.articles.map(article => `- [${label(article.title)}](${page(article)})`), ''])]
writeFileSync(new URL('../articles.md', import.meta.url), [
  '# 文章索引', '', '技术实践、源码阅读与读书笔记。可以通过左侧分类或全文搜索查找文章。', '',
  ...section('技术实践', category => !technical.has(category)),
  ...section('阅读与成长', category => technical.has(category)),
].join('\n'))
