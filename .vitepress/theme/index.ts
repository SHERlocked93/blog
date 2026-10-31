import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import './custom.css'

// 沿用默认主题，通过首页插槽和局部样式调整展示。
export default {
  extends: DefaultTheme,
  Layout
}
