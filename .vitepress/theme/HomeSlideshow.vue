<script setup lang="ts">
import { computed, onMounted, onUnmounted, shallowRef, watch } from 'vue'
import { withBase } from 'vitepress'
import photos from '../data/home-photos.json'

// 首图保持服务端与浏览器一致；后续随机遍历整个相册。
const interval = 7000
const active = shallowRef(0)
const autoplay = shallowRef(true)
const hovered = shallowRef(false)
const focused = shallowRef(false)
const hidden = shallowRef(false)
const mounted = shallowRef(false)
const photo = computed(() => photos[active.value])
const playing = computed(() => mounted.value && autoplay.value && !hovered.value && !focused.value && !hidden.value)
// 待播放队列逐轮洗牌，实际历史用于返回刚才看过的照片。
let queue: number[] = []
const history: number[] = []
let timer: ReturnType<typeof setTimeout> | undefined
let motionQuery: MediaQueryList | undefined

function prepareQueue() {
  if (queue.length) return
  queue = photos.map((_, index) => index).filter(index => index !== active.value)
  for (let index = queue.length - 1; index > 0; index--) {
    const other = Math.floor(Math.random() * (index + 1))
    ;[queue[index], queue[other]] = [queue[other], queue[index]]
  }
}

function schedule() {
  // 恢复播放或手动切换后重新计时，只预加载下一张照片。
  clearTimeout(timer)
  timer = undefined
  if (!playing.value) return
  prepareQueue()
  const upcoming = new Image()
  upcoming.decoding = 'async'
  upcoming.fetchPriority = 'low'
  upcoming.src = withBase(photos[queue[queue.length - 1]].src)
  timer = setTimeout(nextPhoto, interval)
}

function showPhoto(index: number, remember = true) {
  if (index !== active.value && remember) {
    history.push(active.value)
    if (history.length > 50) history.shift()
    queue = queue.filter(candidate => candidate !== index)
  }
  active.value = index
  schedule()
}

function nextPhoto() {
  prepareQueue()
  showPhoto(queue.pop()!)
}

function previousPhoto() {
  const previous = history.pop() ?? (active.value + photos.length - 1) % photos.length
  showPhoto(previous, false)
}

function leaveFocus(event: FocusEvent) {
  // 焦点在轮播内部移动时保持暂停，离开整组控件才恢复。
  const container = event.currentTarget as HTMLElement
  focused.value = event.relatedTarget instanceof Node && container.contains(event.relatedTarget)
}

function updateVisibility() {
  hidden.value = document.hidden
}

function respectMotionPreference() {
  if (motionQuery?.matches) autoplay.value = false
}

watch(playing, schedule)

onMounted(() => {
  motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  respectMotionPreference()
  motionQuery.addEventListener('change', respectMotionPreference)
  updateVisibility()
  document.addEventListener('visibilitychange', updateVisibility)
  mounted.value = true
})

onUnmounted(() => {
  clearTimeout(timer)
  document.removeEventListener('visibilitychange', updateVisibility)
  motionQuery?.removeEventListener('change', respectMotionPreference)
})
</script>

<template>
  <section
    class="home-slideshow"
    role="region"
    aria-roledescription="轮播图"
    aria-label="旅行风景照片"
    :data-playing="playing"
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
    @focusin="focused = true"
    @focusout="leaveFocus"
    @keydown.left.prevent="previousPhoto"
    @keydown.right.prevent="nextPhoto"
  >
    <div class="photo-stage">
      <Transition name="photo-fade">
        <img :key="photo.src" class="slide-photo" :src="withBase(photo.src)" :alt="photo.alt" :width="photo.width" :height="photo.height" fetchpriority="high" />
      </Transition>
    </div>
    <div class="slideshow-footer">
      <p class="photo-location" :aria-live="playing ? 'off' : 'polite'" aria-atomic="true">
        {{ photo.country }}<span aria-hidden="true"> · </span>{{ photo.place }}
      </p>
      <div class="slideshow-controls">
        <button type="button" class="control" aria-label="上一张照片" @click="previousPhoto">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 6-6 6 6 6" /></svg>
        </button>
        <button type="button" class="control" aria-label="下一张照片" @click="nextPhoto">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m10 6 6 6-6 6" /></svg>
        </button>
        <button type="button" class="control playback" :aria-label="autoplay ? '暂停轮播' : '播放轮播'" @click="autoplay = !autoplay">
          <svg v-if="autoplay" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12" /></svg>
          <svg v-else viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 10 7-10 7Z" /></svg>
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-slideshow {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 8px 8px 0;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  background: var(--blog-photo-frame);
  box-shadow: 0 16px 48px rgb(25 57 44 / 9%);
}

.photo-stage {
  position: relative;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  border-radius: 13px;
  background: var(--vp-c-bg-soft);
}

.slide-photo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.slideshow-footer {
  display: flex;
  flex: 0 0 66px;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 0 8px 0 12px;
}

.photo-location {
  min-width: 0;
  color: var(--vp-c-text-1);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.6;
}

.photo-location span {
  padding: 0 4px;
  color: var(--vp-c-text-2);
}

.slideshow-controls {
  display: flex;
  flex-shrink: 0;
}

.control {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  color: var(--vp-c-text-2);
  cursor: pointer;
}

.control:hover {
  background: var(--vp-c-default-soft);
  color: var(--vp-c-brand-1);
}

.control:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: -3px;
}

.playback {
  margin-left: 4px;
  background: var(--vp-c-default-soft);
}

.control svg {
  width: 19px;
  height: 19px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
}

.photo-fade-enter-active,
.photo-fade-leave-active {
  transition: opacity 450ms ease;
}

.photo-fade-enter-from,
.photo-fade-leave-to {
  opacity: 0;
}

@media (max-width: 639px) {
  .home-slideshow {
    padding: 6px 6px 0;
    border-radius: 16px;
  }

  .photo-stage {
    border-radius: 10px;
  }

  .slideshow-footer {
    flex-basis: 64px;
    padding: 0 0 0 6px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .photo-fade-enter-active,
  .photo-fade-leave-active {
    transition: none;
  }
}
</style>
