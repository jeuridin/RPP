"""Создание схемы и пакетная загрузка рейсов в PostgreSQL."""

import os
from datetime import date
from pathlib import Path

from sqlalchemy import (
    Column, DateTime, Integer, MetaData, Numeric, String, Table, BigInteger,
    CheckConstraint, create_engine, text,
)
from dotenv import load_dotenv

load_dotenv()

from generate_flights import generate_flights

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://airline:airline_password@localhost:5432/airline",
)
START_DATE = date.fromisoformat(os.getenv("START_DATE", "2026-11-08"))
DAYS = int(os.getenv("FLIGHT_DAYS", "120"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5000"))

metadata = MetaData()

flights = Table(
    "flights",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("carrier", String(100), nullable=False),
    Column("flight_number", String(20), nullable=False),
    Column("origin", String(3), nullable=False),
    Column("destination", String(3), nullable=False),
    Column("departure_time", DateTime, nullable=False),
    Column("arrival_time", DateTime, nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    CheckConstraint("origin <> destination", name="chk_different_airports"),
    CheckConstraint("arrival_time > departure_time", name="chk_arrival_after_departure"),
)

def main():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    # Создание таблицы и индексов, если они ещё не существуют.
    metadata.create_all(engine)
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_flights_departure_time
            ON flights (departure_time)
        """))
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_flights_route_departure
            ON flights (origin, destination, departure_time)
        """))

    generated = generate_flights(START_DATE, DAYS)
    inserted = 0

    # Одна транзакция на всю загрузку; вставка выполняется пачками.
    with engine.begin() as connection:
        batch = []
        for flight in generated:
            batch.append(flight)
            if len(batch) >= BATCH_SIZE:
                connection.execute(flights.insert(), batch)
                inserted += len(batch)
                batch.clear()

        if batch:
            connection.execute(flights.insert(), batch)
            inserted += len(batch)

    print(f"Загрузка завершена. Добавлено рейсов: {inserted}")
    print(f"Период: {START_DATE} - {START_DATE.fromordinal(START_DATE.toordinal() + DAYS - 1)}")
    engine.dispose()


if __name__ == "__main__":
    main()
