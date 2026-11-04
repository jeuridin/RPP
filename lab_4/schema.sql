CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    carrier VARCHAR(50) NOT NULL,
    flight_number VARCHAR(20) NOT NULL,
    departure_airport VARCHAR(3) NOT NULL,
    arrival_airport VARCHAR(3) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    price NUMERIC(10, 2) NOT NULL
        CHECK (price > 0),
    CHECK (departure_airport <> arrival_airport),
    CHECK (arrival_time > departure_time)
);

CREATE INDEX IF NOT EXISTS idx_flights_departure_date
ON flights (departure_time);