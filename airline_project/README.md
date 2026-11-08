# Агрегатор авиаперелётов: задача 3.1

## 1. Подготовка

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

На Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Создание базы

Скопируйте `.env.example` в `.env`, при необходимости измените параметры подключения.
Загрузчик автоматически читает файл `.env` через `python-dotenv`.
Создайте в PostgreSQL базу `airline` и пользователя с указанными параметрами.

Примените SQL-схему:

```bash
psql -U airline -d airline -f database/schema.sql
```

Либо просто запустите загрузчик: он сам создаст таблицу и индексы.

## 3. Генерация и загрузка

Из корня проекта:

```bash
python database/generate_flights.py
python database/load_flights.py
```

По умолчанию создаются 1500 рейсов в сутки на 120 дней, всего 180 000 рейсов.

Начальная дата фиксирована: `2026-11-08`. Это сделано специально, чтобы повторный запуск
генератора давал тот же набор рейсов. Для другого периода укажите дату явно:

```bash
python database/generate_flights.py --start-date 2027-01-01 --days 120
```

Для загрузчика можно изменить `START_DATE`, `FLIGHT_DAYS` и `DATABASE_URL`
в переменных окружения.

## 4. Проверка результата

```sql
SELECT COUNT(*) FROM flights;

SELECT
    DATE(departure_time) AS flight_date,
    COUNT(*) AS flights_count
FROM flights
GROUP BY DATE(departure_time)
ORDER BY flight_date;

SELECT *
FROM flights
WHERE departure_time >= TIMESTAMP '2026-11-08 00:00:00'
  AND departure_time <  TIMESTAMP '2026-11-09 00:00:00'
ORDER BY departure_time
LIMIT 20;
```

Ожидаемый результат: 180 000 строк, по 1500 рейсов на каждый из 120 дней.

## Примечание

Время хранится как `TIMESTAMP` без часового пояса: в учебной модели все времена
трактуются как локальное время аэропорта в рамках одной условной временной шкалы.
Для реальной международной системы потребовались бы часовые пояса аэропортов.
