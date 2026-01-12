# Переменные
CC=python3
VENVNAME=.venv
REQFILE=requirements.txt

# Основные цели
# all: venv req docker-setup run
all: docker-setup

# # Виртуальное окружение (для локальной разработки)
# venv:
# 	test -d $(VENVNAME) || $(CC) -m venv $(VENVNAME)

# # Установка зависимостей
# req:
# 	pip install -r $(REQFILE)

# # Локальный запуск
# run:
# 	@$(MAKE) -C src

# Docker команды
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

# Комбинации команд
docker-setup: docker-build docker-up

.PHONY: all venv req run docker-build docker-up docker-down docker-setup