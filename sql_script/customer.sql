CREATE TABLE customer_car_registration(
    registration_id VARCHAR(16) PRIMARY KEY NOT NULL,
    car_id INTEGER REFERENCES catalog_car(id)
);

CREATE TYPE customer_marital_status AS ENUM ('single', 'couple', 'married', 'divorced', 'widowed');
CREATE TYPE customer_gender AS ENUM ('M', 'F');
CREATE TABLE customer(
    customer_id SERIAL PRIMARY KEY,
    age INTEGER CHECK (age >= 18 AND age <= 100),
    gender customer_gender,
    debt_rate NUMERIC CHECK (debt_rate >= 0),
    income NUMERIC GENERATED ALWAYS AS (ROUND(debt_rate / 0.3, 2)) STORED,
    marital_status customer_marital_status,
    dependent_children INTEGER CHECK (dependent_children >= 0),
    has_second_car BOOLEAN,
    current_registration_id VARCHAR(255) REFERENCES customer_car_registration(registration_id),

    UNIQUE (age, gender, debt_rate, marital_status, dependent_children, has_second_car)
);
CREATE TABLE customer_marketing(
    id SERIAL PRIMARY KEY,
    age NUMERIC CHECK (age >= 18),
    gender customer_gender,
    debt_rate NUMERIC CHECK (debt_rate >= 0),
    income NUMERIC GENERATED ALWAYS AS (ROUND(debt_rate / 0.3, 2)) STORED,
    marital_status customer_marital_status,
    dependent_children NUMERIC CHECK (dependent_children >= 0),
    has_second_car BOOLEAN,

    UNIQUE (age, gender, debt_rate, marital_status, dependent_children, has_second_car)
);

SELECT cus.*, car.* FROM customer as cus
JOIN customer_car_registration as reg
ON cus.current_registration_id = reg.registration_id
JOIN catalog_car as car
ON reg.car_id = car.id
