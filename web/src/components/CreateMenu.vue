<template>
  <div class="create-menu-float">
    <!-- 触发按钮 -->
    <button class="create-trigger" @click="toggleMenu" :title="isOpen ? '关闭菜单' : '新建内容'">
      <i :class="isOpen ? 'fa-solid fa-times' : 'fa-solid fa-plus'"></i>
    </button>

    <!-- 菜单选项 -->
    <transition name="menu-fade">
      <div v-if="isOpen" class="create-options">
        <button class="create-option" @click="handleCreateMovie">
          <i class="fa-solid fa-film"></i>
          <span>新增影片</span>
        </button>
        <button class="create-option" @click="handleCreateActor">
          <i class="fa-solid fa-user-plus"></i>
          <span>新增演员</span>
        </button>
        <button class="create-option" @click="handleCreatePost">
          <i class="fa-solid fa-pen-to-square"></i>
          <span>新建博客</span>
        </button>
        <button class="create-option" @click="handleUploadImage">
          <i class="fa-solid fa-image"></i>
          <span>上传图片</span>
        </button>
      </div>
    </transition>

    <!-- 遮罩层 -->
    <div v-if="isOpen" class="menu-overlay" @click="closeMenu"></div>
  </div>
</template>

<script>
export default {
  name: 'CreateMenu',
  data() {
    return {
      isOpen: false,
    }
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen
    },
    closeMenu() {
      this.isOpen = false
    },
    handleCreateMovie() {
      this.$eventBus.emit('open-movie-dialog')
      this.closeMenu()
    },
    handleCreateActor() {
      this.$eventBus.emit('open-actor-dialog')
      this.closeMenu()
    },
    handleCreatePost() {
      this.$eventBus.emit('open-post-dialog')
      this.closeMenu()
    },
    handleUploadImage() {
      this.$eventBus.emit('open-image-dialog')
      this.closeMenu()
    },
  },
}
</script>

<style scoped>
/* 触发按钮 */
.create-trigger {
  position: fixed;
  right: 20px;
  bottom: 150px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary-gradient);
  color: white;
  border: none;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 998;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.create-trigger:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-hover);
}

.create-trigger i {
  transition: transform 0.3s ease;
}

.create-trigger:hover i {
  transform: rotate(90deg);
}

/* 遮罩层 */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 997;
}

/* 菜单选项 */
.create-options {
  position: fixed;
  right: 20px;
  bottom: 220px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 998;
}

.create-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  background: var(--card-bg);
  border: 2px solid var(--border-light);
  border-radius: 28px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
  min-width: 150px;
}

.create-option:hover {
  transform: translateX(-5px);
  border-color: var(--primary-color);
  box-shadow: var(--shadow-lg);
  background: var(--bg-gradient-light);
}

.create-option i {
  font-size: 18px;
  width: 20px;
  text-align: center;
  color: var(--primary-color);
}

/* 动画 */
.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: all 0.3s ease;
}

.menu-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.menu-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 只在移动端显示 */
@media (min-width: 769px) {
  .create-menu-float {
    display: none;
  }
}

/* 移动端样式调整 */
@media (max-width: 768px) {
  .create-trigger {
    right: 15px;
    bottom: 140px;
    width: 50px;
    height: 50px;
    font-size: 20px;
  }

  .create-options {
    right: 15px;
    bottom: 205px;
  }

  .create-option {
    padding: 12px 18px;
    font-size: 14px;
    min-width: 140px;
  }

  .create-option i {
    font-size: 16px;
  }
}
</style>
