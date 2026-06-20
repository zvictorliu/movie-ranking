SHELL := /bin/bash

.DEFAULT_GOAL := help

BACKEND_DIR := backend
WEB_DIR := web
BACKEND_PORT ?= 5000
FRONTEND_PORT ?= 5173

.PHONY: help dev backend frontend install install-backend install-frontend content clean

help:
	@echo "可用命令:"
	@echo "  make dev              一键安装依赖并启动前后端"
	@echo "  make backend          只启动后端: http://localhost:$(BACKEND_PORT)"
	@echo "  make frontend         只启动前端: http://localhost:$(FRONTEND_PORT)"
	@echo "  make install          安装前后端依赖"
	@echo "  make content          创建本地 content 目录"
	@echo "  make clean            清理本地依赖目录"
	@echo "  端口示例: make dev BACKEND_PORT=5001 FRONTEND_PORT=5174"

dev: install content
	@echo "启动后端 http://localhost:$(BACKEND_PORT)"
	@cd $(BACKEND_DIR) && BACKEND_PORT=$(BACKEND_PORT) uv run python app.py & \
	BACKEND_PID=$$!; \
	echo "启动前端 http://localhost:$(FRONTEND_PORT)"; \
	cd $(WEB_DIR) && VITE_BACKEND_URL=http://localhost:$(BACKEND_PORT) npm run dev -- --port $(FRONTEND_PORT) & \
	FRONTEND_PID=$$!; \
	trap 'kill $$BACKEND_PID $$FRONTEND_PID 2>/dev/null' INT TERM EXIT; \
	wait $$BACKEND_PID $$FRONTEND_PID

backend: install-backend content
	cd $(BACKEND_DIR) && BACKEND_PORT=$(BACKEND_PORT) uv run python app.py

frontend: install-frontend
	cd $(WEB_DIR) && VITE_BACKEND_URL=http://localhost:$(BACKEND_PORT) npm run dev -- --port $(FRONTEND_PORT)

install: install-backend install-frontend

install-backend:
	cd $(BACKEND_DIR) && uv sync

install-frontend: $(WEB_DIR)/node_modules

$(WEB_DIR)/node_modules: $(WEB_DIR)/package-lock.json
	cd $(WEB_DIR) && npm install

content:
	mkdir -p content/movies content/actors content/posts content/imgbed \
		content/covers/movie-cover content/covers/actor-cover content/covers/post-cover

clean:
	rm -rf $(BACKEND_DIR)/.venv $(WEB_DIR)/node_modules
