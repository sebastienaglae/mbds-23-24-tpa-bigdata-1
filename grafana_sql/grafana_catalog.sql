-- Grafana
-- Table: catalog_car
-- Auteur: Sébastien AGLAE
 -- Catalogue

SELECT *
FROM catalog_car;

--- Nombre de voitures par couleur

SELECT COUNT(*) as total_cars,
       c.color
FROM catalog_car AS c
GROUP BY c.color;

--- Répartition des prix des voitures par couleur

SELECT cc.color,
       AVG(cc.price) AS avg_price
FROM catalog_car cc
GROUP BY cc.color
ORDER BY cc.color;

--- Distribution de la puissance dans les voitures

SELECT power,
       COUNT(*) AS car_count
FROM catalog_car
GROUP BY power
ORDER BY power;

--- Relation entre la puissance et les émissions de CO2

SELECT power,
       AVG(co2_emissions) AS avg_co2_emissions,
       AVG(price) AS avg_price
FROM catalog_car
GROUP BY power;

--- Les 5 voitures les plus longues et avec leur place assise

SELECT DISTINCT name,
                length,
                seating_capacity
FROM catalog_car
ORDER BY length DESC
LIMIT 5;

