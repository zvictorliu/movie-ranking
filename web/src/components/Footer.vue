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
        <a href="#" class="footer-link">
          <span class="material-icons">info</span>
          关于
        </a>
        <a href="#" class="footer-link">
          <span class="material-icons">mail</span>
          联系
        </a>
        <a href="#" class="footer-link">
          <span class="material-icons">help</span>
          帮助
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
  gap: 6px;
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  font-size: 14px;
}

.footer-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.footer-link .material-icons {
  font-size: 18px;
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
    font-size: 13px;
    padding: 6px 10px;
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
