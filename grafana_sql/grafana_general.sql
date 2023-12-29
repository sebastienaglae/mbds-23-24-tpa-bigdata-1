-- Grafana
-- Table: catalog_car
-- Auteur: Sébastien AGLAE
 -- Général

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE';

--- Corrélation entre le revenu et le prix des voitures (0-1000€)

SELECT cu.income AS customer_income,
       AVG(c.price) AS avg_car_price
FROM catalog_car c
JOIN customer_car_registration r ON c.id = r.car_id
JOIN customer cu ON r.registration_id = cu.current_registration_id
WHERE cu.income >= 0
    AND cu.income <= 1000
GROUP BY cu.income
ORDER BY cu.income;

--- Corrélation entre le revenu et le prix des voitures (1001-2200€)

SELECT cu.income AS customer_income,
       AVG(c.price) AS avg_car_price
FROM catalog_car c
JOIN customer_car_registration r ON c.id = r.car_id
JOIN customer cu ON r.registration_id = cu.current_registration_id
WHERE cu.income > 1000
    AND cu.income <= 2200
GROUP BY cu.income
ORDER BY cu.income;

--- Corrélation entre le revenu et le prix des voitures (2201€+)

SELECT cu.income AS customer_income,
       AVG(c.price) AS avg_car_price
FROM catalog_car c
JOIN customer_car_registration r ON c.id = r.car_id
JOIN customer cu ON r.registration_id = cu.current_registration_id
WHERE cu.income > 2200
GROUP BY cu.income
ORDER BY cu.income;

--- Puissance moyenne et émissions de CO2

SELECT cc.power AS avg_power,
       bce.co2_emissions AS avg_co2_emissions
FROM catalog_car cc
JOIN brand_co2_emissions bce ON cc.brand = bce.brand;

--- Répartition des prix des voitures par marque

SELECT brand,
       COUNT(*) AS car_count,
       AVG(price) AS avg_price,
       MIN(price) AS min_price,
       MAX(price) AS max_price
FROM catalog_car
GROUP BY brand;

--- Top 5 des marques de voitures les plus immatriculées

SELECT c.brand,
       COUNT(*) AS registration_count
FROM catalog_car c
JOIN customer_car_registration r ON c.id = r.car_id
GROUP BY c.brand
ORDER BY registration_count DESC
LIMIT 5;

--- Relation entre le prix des voitures et les émissions de CO2 par marque

SELECT cc.brand,
       AVG(cc.price) AS avg_price,
       AVG(bce.co2_emissions) AS avg_co2_emissions,
       COUNT(*) AS car_count
FROM catalog_car cc
JOIN brand_co2_emissions bce ON cc.brand = bce.brand
GROUP BY cc.brand;

--- Revenu moyen et âge par marque de voiture

SELECT c.brand,
       AVG(cu.income) AS avg_income,
       AVG(cu.age) AS avg_age
FROM catalog_car c
JOIN customer_car_registration r ON c.id = r.car_id
JOIN customer cu ON r.registration_id = cu.current_registration_id
GROUP BY c.brand
ORDER BY avg_income DESC;

--- Immatriculation des voitures avec le nombre de places assises et le nombre de portes

SELECT cc.seating_capacity,
       cc.number_doors,
       COUNT(*) AS registration_count
FROM catalog_car cc
JOIN customer_car_registration ccr ON cc.id = ccr.car_id
GROUP BY cc.seating_capacity,
         cc.number_doors;

--- Marques de voitures avec la puissance moyenne la plus élevée

SELECT cc.brand,
       AVG(cc.power) AS avg_power
FROM catalog_car cc
GROUP BY cc.brand
ORDER BY avg_power DESC;

