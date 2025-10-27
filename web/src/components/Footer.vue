<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-info">
        <p class="footer-title">
          <span class="material-icons">movie</span>
          影片排行榜
        </p>
        <p class="footer-copyright">&copy; 2025 Movie Ranking App. All rights reserved.</p>
      </div>
      <div class="footer-links">
        <a href="https://github.com/zvictorliu/movie-ranking" target="_blank" rel="noopener noreferrer" class="footer-link" title="GitHub 项目">
          <i class="fa-brands fa-github"></i>
        </a>
        <a href="mailto:zvictorliu@outlook.com" class="footer-link" title="邮件联系">
          <i class="fa-solid fa-envelope"></i>
        </a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--primary-gradient);
  color: white;
  padding: 30px 20px;
  margin-top: auto;
  box-shadow: var(--shadow-sm);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.footer-title .material-icons {
  font-size: 24px;
}

.footer-copyright {
  font-size: 14px;
  margin: 0;
  opacity: 0.9;
}

.footer-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.footer-link {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 24px;
  width: 40px;
  height: 40px;
}

.footer-link:hover {
  opacity: 0.7;
  transform: scale(1.1);
}

.footer-link i {
  font-size: 24px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-footer {
    padding: 20px 15px;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .footer-info {
    align-items: center;
  }

  .footer-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .footer-link {
    width: 36px;
    height: 36px;
  }

  .footer-link i {
    font-size: 20px;
  }

  .footer-title {
    font-size: 16px;
  }

  .footer-copyright {
    font-size: 12px;
  }
}

/* Dark mode styles are now handled by CSS variables */
</style>

<style>
/* 简洁主题下的 Footer 样式（非 scoped） */
/* 亮色模式 */
body.theme-minimal:not(.dark-mode) .app-footer {
  background: #f8f8f8 !important;
  color: #000000;
}

body.theme-minimal:not(.dark-mode) .footer-title {
  text-shadow: none;
}

body.theme-minimal:not(.dark-mode) .footer-link {
  color: #333333;
}

/* 暗色模式 */
body.theme-minimal.dark-mode .app-footer {
  background: #1a1a1a !important;
  color: #ffffff;
}

body.theme-minimal.dark-mode .footer-title {
  text-shadow: none;
}

body.theme-minimal.dark-mode .footer-link {
  color: #e0e0e0;
}
</style>
