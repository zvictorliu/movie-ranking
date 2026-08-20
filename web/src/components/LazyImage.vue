<template>
  <img
    ref="imgEl"
    :src="currentSrc"
    :alt="alt"
    :class="imgClass"
    loading="lazy"
    decoding="async"
    @error="onError"
    @load="onLoad"
  />
</template>

<script>
const DEFAULT_COVER = '/imgs/default_cover.jpg'
const PLACEHOLDER =
  'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="16" height="9"%3E%3Crect width="16" height="9" fill="%23e8e8e8"/%3E%3C/svg%3E'

export default {
  name: 'LazyImage',
  props: {
    src: {
      type: String,
      default: '',
    },
    alt: {
      type: String,
      default: '',
    },
    imgClass: {
      type: [String, Object, Array],
      default: '',
    },
    rootMargin: {
      type: String,
      default: '200px',
    },
    fallback: {
      type: String,
      default: DEFAULT_COVER,
    },
  },
  data() {
    return {
      isVisible: false,
      hasError: false,
      observer: null,
    }
  },
  computed: {
    currentSrc() {
      if (this.hasError) {
        return this.fallback
      }
      if (!this.isVisible) {
        return PLACEHOLDER
      }
      return this.src || this.fallback
    },
  },
  watch: {
    src() {
      this.hasError = false
    },
  },
  mounted() {
    this.setupObserver()
  },
  beforeUnmount() {
    this.teardownObserver()
  },
  methods: {
    setupObserver() {
      const el = this.$refs.imgEl
      if (!el) return

      if (typeof IntersectionObserver === 'undefined') {
        this.isVisible = true
        return
      }

      this.observer = new IntersectionObserver(
        (entries) => {
          const entry = entries[0]
          if (entry && entry.isIntersecting) {
            this.isVisible = true
            this.teardownObserver()
          }
        },
        { rootMargin: this.rootMargin },
      )
      this.observer.observe(el)
    },
    teardownObserver() {
      if (this.observer) {
        this.observer.disconnect()
        this.observer = null
      }
    },
    onError() {
      if (this.hasError) return
      this.hasError = true
    },
    onLoad() {
      // no-op; kept for potential future fade-in hooks
    },
  },
}
</script>
