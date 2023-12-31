CREATE TABLE catalog_car_category (
    id INTEGER PRIMARY KEY -- from 0 to .. (number of categories - 1)
    name VARCHAR(32) NOT NULL
);

CREATE TYPE catalog_car_length AS ENUM ('short', 'medium', 'long', 'very_long');
CREATE TYPE catalog_car_color AS ENUM ('white', 'blue', 'grey', 'black', 'red');
CREATE TABLE catalog_car (
    id SERIAL PRIMARY KEY,
    category_id integer REFERENCES catalog_car_category(id),

    brand VARCHAR(32) NOT NULL,
    name VARCHAR(255) NOT NULL,
    power integer NOT NULL CHECK (power >= 50 AND power <= 1500),
    length catalog_car_length NOT NULL,
    seating_capacity integer NOT NULL CHECK (seating_capacity >= 2 AND seating_capacity <= 9),
    number_doors integer NOT NULL CHECK (number_doors >= 3 AND number_doors <= 5),
    color catalog_car_color NOT NULL,
    used BOOLEAN,

    price NUMERIC NOT NULL CHECK (price >= 5000 AND price <= 150000),

    -- attributes computed from co2.csv
    bonus_malus NUMERIC,
    co2_emissions NUMERIC,
    energy_cost NUMERIC,

    -- tuple (category_id, brand, name, power, length, seating_capacity, number_doors, color, used) allow us to retrieve the car from datalake
    UNIQUE (brand, name, power, length, seating_capacity, number_doors, color, used)
);

