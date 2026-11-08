"""Детерминированная генерация рейсов собственной авиакомпании."""

import argparse
import random
from datetime import date, datetime, time, timedelta
from decimal import Decimal

AIRPORTS = [
    "SVO", "DME", "VKO", "LED", "KZN", "SVX", "OVB", "KRR", "AER", "ROV",
    "UFA", "GOJ", "KUF", "CEK", "OMS", "IKT", "KJA", "VVO", "KGD", "MMK",
    "MRV", "NAL", "UUS", "BAX", "PEE", "TJM", "NOZ", "GDX", "DYU", "EVN",
]

CARRIER = "OwnAir"
FLIGHTS_PER_DAY = 1500
DAYS = 120
BASE_SEED = 20261108


def generate_flights(start_date: date, days: int = DAYS, seed: int = BASE_SEED):
    """Возвращает одинаковый набор рейсов при одинаковых аргументах."""
    for day_offset in range(days):
        flight_date = start_date + timedelta(days=day_offset)
        # Отдельный seed для каждого дня делает результат независимым от порядка обхода.
        rng = random.Random(f"{seed}:{flight_date.isoformat()}")

        for number in range(1, FLIGHTS_PER_DAY + 1):
            origin = rng.choice(AIRPORTS)
            destination = rng.choice(AIRPORTS)
            while destination == origin:
                destination = rng.choice(AIRPORTS)

            departure_minutes = rng.randrange(0, 24 * 60)
            departure = datetime.combine(flight_date, time.min) + timedelta(
                minutes=departure_minutes
            )
            duration_minutes = rng.randint(60, 360)
            arrival = departure + timedelta(minutes=duration_minutes)

            # Номер и цена воспроизводимы, поскольку используются те же seed и порядок.
            price = Decimal(rng.randrange(3500, 45001)).quantize(Decimal("0.01"))

            yield {
                "carrier": CARRIER,
                "flight_number": f"OA{day_offset + 1:03d}{number:04d}",
                "origin": origin,
                "destination": destination,
                "departure_time": departure,
                "arrival_time": arrival,
                "price": price,
            }


def main():
    parser = argparse.ArgumentParser(description="Генератор рейсов на 120 дней")
    parser.add_argument(
        "--start-date",
        default="2026-11-08",
        help="Начальная дата в формате YYYY-MM-DD (по умолчанию 2026-11-08)",
    )
    parser.add_argument("--days", type=int, default=DAYS)
    parser.add_argument("--seed", type=int, default=BASE_SEED)
    args = parser.parse_args()

    start_date = date.fromisoformat(args.start_date)
    if args.days <= 0:
        parser.error("--days должен быть положительным")

    flights = list(generate_flights(start_date, args.days, args.seed))
    print(f"Сгенерировано рейсов: {len(flights)}")
    print(f"Период: {start_date} - {start_date + timedelta(days=args.days - 1)}")
    print(f"Первый рейс: {flights[0]}")
    print(f"Последний рейс: {flights[-1]}")


if __name__ == "__main__":
    main()
