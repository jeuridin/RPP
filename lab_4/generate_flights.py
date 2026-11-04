
import random
from datetime import datetime, timedelta, date
import psycopg2
from psycopg2.extras import execute_values

# Фиксируем генератор случайных чисел
random.seed(42)

# Параметры генерации
START_DATE = date(2026, 1, 1)
DAYS = 120
FLIGHTS_PER_DAY = 1500

AIRPORTS = [
    "OVB", "SVO", "DME", "VKO", "LED",
    "KZN", "AER", "SVX", "KRR", "ROV",
    "UFA", "CEK", "OMS", "KJA", "IKT",
    "VVO", "KHV", "GOJ", "MRV", "KGD",
    "TJM", "PEE", "NOZ", "BAX", "GSV",
    "UUS", "HTA", "YKS", "PKC", "NAL"
]

CARRIERS = [
    "Aeroflot",
    "S7 Airlines",
    "Ural Airlines",
    "Pobeda",
    "Smartavia"
]


def generate_flights():
    flights = []

    for day in range(DAYS):
        current_date = START_DATE + timedelta(days=day)

        for number in range(FLIGHTS_PER_DAY):
            departure_airport = random.choice(AIRPORTS)

            # Аэропорт прилёта не должен совпадать с аэропортом вылета
            arrival_airport = random.choice(
                [a for a in AIRPORTS if a != departure_airport]
            )

            carrier = random.choice(CARRIERS)

            flight_number = (
                f"{CARRIERS.index(carrier) + 1}"
                f"{random.randint(100, 9999)}"
            )

            # Вылет в пределах первых 18 часов суток
            departure_minutes = random.randint(0, 18 * 60)

            departure_time = datetime.combine(
                current_date, datetime.min.time()
            ) + timedelta(minutes=departure_minutes)

            # Продолжительность полёта от 1 до 6 часов
            duration = random.randint(1, 6)

            arrival_time = departure_time + timedelta(
                hours=duration
            )

            price = round(random.uniform(3000, 30000), 2)

            flights.append((
                carrier,
                flight_number,
                departure_airport,
                arrival_airport,
                departure_time,
                arrival_time,
                price
            ))

    return flights


def load_flights():
    connection = psycopg2.connect(
        dbname="flights_db",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )

    try:
        with connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS flights (
                        id SERIAL PRIMARY KEY,
                        carrier VARCHAR(50) NOT NULL,
                        flight_number VARCHAR(20) NOT NULL,
                        departure_airport VARCHAR(3) NOT NULL,
                        arrival_airport VARCHAR(3) NOT NULL,
                        departure_time TIMESTAMP NOT NULL,
                        arrival_time TIMESTAMP NOT NULL,
                        price NUMERIC(10, 2) NOT NULL,
                        CHECK (price > 0),
                        CHECK (
                            departure_airport <> arrival_airport
                        ),
                        CHECK (arrival_time > departure_time)
                    );
                """)

                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS
                    idx_flights_departure_date
                    ON flights (departure_time);
                """)

                # Удаляем предыдущую генерацию
                cursor.execute("""
                    TRUNCATE TABLE flights RESTART IDENTITY;
                """)

                flights = generate_flights()

                # Загружаем данные пакетами
                execute_values(
                    cursor,
                    """
                    INSERT INTO flights (
                        carrier,
                        flight_number,
                        departure_airport,
                        arrival_airport,
                        departure_time,
                        arrival_time,
                        price
                    ) VALUES %s
                    """,
                    flights,
                    page_size=5000
                )

                print(f"Загружено рейсов: {len(flights)}")

    finally:
        connection.close()


if __name__ == "__main__":
    load_flights()
