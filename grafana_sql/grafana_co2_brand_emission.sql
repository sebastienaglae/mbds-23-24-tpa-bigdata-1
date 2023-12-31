-- Grafana
-- Table: catalog_car
-- Auteur: Sébastien AGLAE
 -- Emissions de CO2 Marque

SELECT *
FROM brand_co2_emissions;

--- Nombre total de voitures par marque

SELECT brand,
       COUNT(*)
FROM brand_co2_emissions
GROUP BY brand
ORDER BY COUNT(*) DESC;

--- Émissions de CO2 moyennes par marque

SELECT brand,
       AVG(co2_emissions)
FROM brand_co2_emissions
WHERE co2_emissions > 0
GROUP BY brand
ORDER BY AVG(co2_emissions);

--- Coût moyen de l'énergie par marque de voiture

SELECT brand,
       AVG(energy_cost) AS avg_energy_cost
FROM brand_co2_emissions
GROUP BY brand
ORDER BY avg_energy_cost DESC;

--- Distribution des valeurs de bonus/malus

SELECT CASE
           WHEN bonus_malus >= 0 THEN 'B'
           WHEN bonus_malus < 0 THEN 'M'
           ELSE 'N'
       END AS bonus_malus_category,
       COUNT(*) AS count
FROM brand_co2_emissions
GROUP BY bonus_malus_category;

--- Top 3 des modèles de voitures ayant les coûts énergétiques les plus bas

SELECT CONCAT(brand, ' ', car_name) AS brand_car_name,
       energy_cost
FROM brand_co2_emissions
ORDER BY energy_cost ASC
LIMIT 3;

--- Répartition des émissions de CO2

SELECT CASE
           WHEN co2_emissions >= 0
                AND co2_emissions <= 100 THEN '0-100'
           WHEN co2_emissions > 100
                AND co2_emissions <= 200 THEN '101-200'
           WHEN co2_emissions > 200
                AND co2_emissions <= 300 THEN '201-300'
           WHEN co2_emissions > 300
                AND co2_emissions <= 400 THEN '301-400'
           WHEN co2_emissions > 400
                AND co2_emissions <= 500 THEN '301-400'
           WHEN co2_emissions > 500 THEN '500+'
           ELSE 'N'
       END AS co2_emissions_range,
       COUNT(*) AS count
FROM brand_co2_emissions
WHERE co2_emissions IS NOT NULL
GROUP BY co2_emissions_range
ORDER BY co2_emissions_range;

--- Rapport bonus/malus par marque de voiture

SELECT brand,
       COUNT(bonus_malus) AS with_bonus_malus
FROM brand_co2_emissions
GROUP BY brand
ORDER BY with_bonus_malus;

--- Top 3 des modèles de voitures ayant les coûts énergétiques les plus élevés

SELECT CONCAT(brand, ' ', car_name) AS brand_car_name,
       energy_cost
FROM brand_co2_emissions
ORDER BY energy_cost DESC
LIMIT 3;