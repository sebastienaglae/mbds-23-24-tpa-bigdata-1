-- Grafana
-- Table: catalog_car
-- Auteur: Sébastien AGLAE
 -- Marketing

SELECT *
FROM customer_marketing;

--- Répartition des tranches d'âges dans les données de marketing
 
SELECT CASE 
           WHEN age BETWEEN 18 AND 25 THEN '18-25' 
           WHEN age BETWEEN 26 AND 35 THEN '26-35' 
           WHEN age BETWEEN 36 AND 45 THEN '36-45' 
           ELSE '46+'
       END AS age_group,
       COUNT(*) AS count
FROM customer_marketing
GROUP BY age_group
ORDER BY age_group;

--- Répartition des sexes dans le secteur du marketing

SELECT gender,
       COUNT(*) AS count
FROM customer_marketing
GROUP BY gender;

--- Répartition des enfants à charge dans le marketing

SELECT dependent_children,
       COUNT(*) AS count
FROM customer_marketing
GROUP BY dependent_children
ORDER BY dependent_children;

--- Répartition des clients par fourchette de taux d'endettement dans le secteur du marketing

SELECT ROUND(debt_rate / 100) * 100 AS debt_range,
       COUNT(*) AS count
FROM customer_marketing
GROUP BY debt_range
ORDER BY debt_range;

--- Top 5 des groupes d'âge ayant les revenus les plus élevés en marketing

SELECT age,
       MAX(income) AS max_income
FROM customer_marketing
GROUP BY age
ORDER BY max_income DESC
LIMIT 5;