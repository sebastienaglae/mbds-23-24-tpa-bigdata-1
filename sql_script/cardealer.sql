----------------------------------------------
-- CAR DEALER TABLE (Catalogue)
----------------------------------------------

-- Table "Catalogue" :
-- marque (chaîne de caractères)
-- nom (chaîne de caractères)
-- puissance (nombre)
-- longueur (nombre)
-- nbPlaces (nombre)
-- nbPortes (nombre)
-- couleur (chaîne de caractères)
-- occasion (booléen, par exemple True/False)
-- prix (nombre)
-- bonusMalus (nombre)
-- rejetCO2 (nombre)
-- coutEnergie (nombre)

CREATE TABLE car_dealer (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(255),
    car_name VARCHAR(255),
    power NUMERIC,
    car_length NUMERIC,
    seating_capacity NUMERIC,
    number_doors NUMERIC,
    color VARCHAR(255),
    used BOOLEAN,
    price NUMERIC,
    bonus_malus NUMERIC,
    co2_emissions NUMERIC,
    energy_cost NUMERIC
);