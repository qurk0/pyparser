include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help load start stop dump reset


help:
	@echo " - load file={имя_файла} - выгрузка данных из .html или .csv в БД"
	@echo " - start     - запускает docker-контейнер с БД"
	@echo " - restore   - возобновляет работу остановленного docker-контейнера"
	@echo " - stop      - останавливает контейнер"
	@echo " - dump      - делает дамп БД"
	@echo " - reset     - пересоздаёт контейнер с нуля"
	@echo " - disc      - добавление новой дисциплины в БД"

start:
	docker compose up -d

stop:
	@echo "Останавливаю контейнер $(DB_CONTAINER)..."
	docker stop $(DB_CONTAINER)

restore:
	docker start $(DB_CONTAINER)

dump: 
	docker exec python_markparser-postgres-1 pg_dump -U myuser mydb -f /tmp/dump.sql
	docker cp python_markparser-postgres-1:/tmp/dump.sql ./dump.sql

reset:
	@echo "Пересоздаю контейнер $(DB_CONTAINER)..."
	docker compose down -v
	docker compose up -d --build

load:
	@echo "Загружаем файл: $(file)"
	python3 main.py $(file)

disc:
	python3 ra_disc.py