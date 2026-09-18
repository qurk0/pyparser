include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help load start stop restore dump reset disc seed wait-db

help:
	@echo " - load file={имя_файла} - загрузка данных из .html или .csv в БД"
	@echo " - start     - запускает БД"
	@echo " - restore   - запускает ранее остановленную БД"
	@echo " - stop      - останавливает БД"
	@echo " - dump      - делает дамп БД"
	@echo " - reset     - пересоздаёт БД с нуля"
	@echo " - disc      - добавляет новую дисциплину в БД"
	@echo " - seed - загружает данные из dump.sql в БД"

start:
	docker compose up -d
	$(MAKE) wait-db

stop:
	docker compose stop postgres

restore:
	docker compose start postgres

dump:
	docker compose exec -T postgres pg_dump -U $(DB_USER) $(DB_NAME) > dump.sql

reset:
	docker compose down -v
	docker compose up -d --build
	$(MAKE) wait-db

load:
	python3 main.py $(file)

disc:
	python3 ra_disc.py

seed:
	docker compose exec -T postgres psql -U $(DB_USER) -d $(DB_NAME) < seed.sql

wait-db:
	@until docker compose exec -T postgres pg_isready -U $(DB_USER) -d $(DB_NAME) > /dev/null 2>&1; do \
		echo "Ожидание PostgreSQL..."; \
		sleep 1; \
	done
	@echo "PostgreSQL готов."