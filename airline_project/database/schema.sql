CREATE TABLE IF NOT EXISTS flights (
    id BIGSERIAL PRIMARY KEY,
    carrier VARCHAR(100) NOT NULL,
    flight_number VARCHAR(20) NOT NULL,
    origin VARCHAR(3) NOT NULL,
    destination VARCHAR(3) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    CONSTRAINT chk_different_airports CHECK (origin <> destination),
    CONSTRAINT chk_arrival_after_departure CHECK (arrival_time > departure_time)
);

-- Индекс по времени вылета позволяет быстро выбирать рейсы за конкретную дату.
CREATE INDEX IF NOT EXISTS idx_flights_departure_time
    ON flights (departure_time);

-- Дополнительный индекс помогает искать рейсы по направлению.
CREATE INDEX IF NOT EXISTS idx_flights_route_departure
    ON flights (origin, destination, departure_time);
