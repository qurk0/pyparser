include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help load start stop restore dump reset disc

help:
	@echo " - load file={имя_файла} - загрузка данных из .html или .csv в БД"
	@echo " - start     - запускает БД"
	@echo " - restore   - запускает ранее остановленную БД"
	@echo " - stop      - останавливает БД"
	@echo " - dump      - делает дамп БД"
	@echo " - reset     - пересоздаёт БД с нуля"
	@echo " - disc      - добавляет новую дисциплину в БД"

start:
	docker compose up -d

stop:
	docker compose stop postgres

restore:
	docker compose start postgres

dump:
	docker compose exec -T postgres pg_dump -U $(DB_USER) $(DB_NAME) > dump.sql

reset:
	docker compose down -v
	docker compose up -d --build

load:
	python3 main.py $(file)

disc:
	python3 ra_disc.py