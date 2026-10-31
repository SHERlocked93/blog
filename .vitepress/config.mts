import { defineConfig } from 'vitepress'
import { readFileSync } from 'node:fs'

// 文章清单同时用于分类索引和默认主题侧栏
const catalog = JSON.parse(readFileSync(new URL('./data/articles.json', import.meta.url), 'utf8'))
const visible = catalog.articles.filter((article: { excluded?: boolean }) => !article.excluded)
const categories = catalog.categories as string[]
// 仅对有明确缺项记录的旧图片显示提示，未声明的资源错误仍由构建检查拦截
const missingImages = new Set(JSON.parse(readFileSync(new URL('./data/missing-images.json', import.meta.url), 'utf8'))
  .map((image: { source: string }) => image.source))

export default defineConfig({
  lang: 'zh-CN',
  title: 'SHERlocked93 个人博客',
  description: '做程序员，不做码农。技术实践、源码阅读与读书笔记。',
  base: '/blog/',
  cleanUrls: false,
  markdown: {
    config(md) {
      const image = md.renderer.rules.image!
      md.renderer.rules.image = (tokens, index, options, env, self) => {
        const token = tokens[index]
        if (missingImages.has(token.attrGet('src') || '')) {
          return `<span role="img" aria-label="原图待恢复">[图片待恢复：${md.utils.escapeHtml(token.content || '原图')}]</span>`
        }
        return image(tokens, index, options, env, self)
      }
    }
  },
  srcExclude: ['README.md', 'scripts/**', 'tests/**', 'migration/**', '.migration-cache/**', 'memory-bank/**',
    '.obsidian/**', 'Docs/*.html.md',
    ...catalog.articles.filter((article: { excluded?: boolean }) => article.excluded)
      .map((article: { file: string }) => article.file)],
  head: [['meta', { name: 'theme-color', content: '#3451b2' }],
    ['link', { rel: 'icon', type: 'image/x-icon', href: '/blog/favicon.ico' }]],
  sitemap: { hostname: 'https://sherlocked93.github.io/blog/' },
  themeConfig: {
    nav: [{ text: '首页', link: '/' }, { text: '文章索引', link: '/articles' }],
    sidebar: [{ text: '文章索引', link: '/articles' }, ...categories.map(category => ({
      text: category,
      collapsed: true,
      items: visible.filter((article: { category: string }) => article.category === category)
        .map((article: { title: string, file: string }) => ({
          text: article.title, link: '/' + article.file.replace(/\.md$/, '.html')
        }))
    }))],
    outline: { label: '本页目录', level: [2, 3] },
    search: { provider: 'local', options: { locales: { root: { translations: {
      button: { buttonText: '搜索文章', buttonAriaLabel: '搜索文章' },
      modal: { noResultsText: '没有找到相关文章', resetButtonTitle: '清除搜索',
        footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' } }
    } } } } },
    socialLinks: [{ icon: 'github', link: 'https://github.com/SHERlocked93/blog' }],
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '文章分类',
    returnToTopLabel: '返回顶部',
    docFooter: { prev: '上一篇', next: '下一篇' },
    footer: { message: '做程序员，不做码农', copyright: 'SHERlocked93' }
  }
})
