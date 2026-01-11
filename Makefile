# Переменные
CC=python3
VENVNAME=.venv
REQFILE=requirements.txt

# Основные цели
all: venv req run

# Виртуальное окружение (для локальной разработки)
venv:
	test -d $(VENVNAME) || $(CC) -m venv $(VENVNAME)

# Установка зависимостей
req:
	pip install -r $(REQFILE)

# Локальный запуск
run:
	@$(MAKE) -C src

# Docker команды
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-up-full:
	docker-compose up

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-logs-api:
	docker-compose logs -f fastapi

docker-logs-rabbit:
	docker-compose logs -f rabbitmq

docker-restart:
	docker-compose restart

docker-status:
	docker-compose ps

docker-clean:
	docker-compose down -v
	docker system prune -f

# Для запуска только RabbitMQ (устаревшее, рекомендуется использовать docker-compose)
docker-rabbitmq-only:
	docker run --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.10.7-management

# Комбинации команд
docker-setup: docker-build docker-up

docker-dev: docker-build docker-up-full

.PHONY: all venv req run docker-build docker-up docker-down docker-logs docker-restart docker-status docker-clean docker-setup docker-dev docker-rabbitmq-only