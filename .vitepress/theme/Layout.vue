<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { withBase } from 'vitepress'
import HomeSlideshow from './HomeSlideshow.vue'

// 使用默认布局提供的首页插槽，文章阅读页继续沿用默认主题。
const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #home-hero-image>
      <HomeSlideshow />
    </template>
    <template #home-features-before>
      <div class="home-topics-heading">
        <h2>文章主题</h2>
        <a :href="withBase('/articles.html')">查看文章索引</a>
      </div>
    </template>
  </Layout>
</template>
