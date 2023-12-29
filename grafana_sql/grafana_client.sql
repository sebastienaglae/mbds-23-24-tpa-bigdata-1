-- Grafana
-- Table: catalog_car
-- Auteur: Sébastien AGLAE
 -- Client

SELECT *
FROM customer;

--- Nombre de clients par tranche d'âge et genre
 
SELECT CASE 
           WHEN cu.age BETWEEN 18 AND 25 THEN '18-25' 
           WHEN cu.age BETWEEN 26 AND 35 THEN '26-35' 
           WHEN cu.age BETWEEN 36 AND 45 THEN '36-45' 
           ELSE '46+' 
       END as age_group, 
       COUNT(*) FILTER (
                        WHERE cu.gender = 'M') as male_customers, 
       COUNT(*) FILTER (
                        WHERE cu.gender = 'F') as female_customers
FROM customer AS cu
GROUP BY age_group;

--- Nombre de clients possédant une deuxième voiture par genre

SELECT cu.has_second_car,
       COUNT(*) FILTER (
                        WHERE cu.gender = 'M') as male_customers,
       COUNT(*) FILTER (
                        WHERE cu.gender = 'F') as female_customers
FROM customer AS cu
GROUP BY cu.has_second_car;

--- Nombre de clients par statut marital et genre

SELECT cu.marital_status,
       COUNT(*) FILTER (
                        WHERE cu.gender = 'M') as male_customers,
       COUNT(*) FILTER (
                        WHERE cu.gender = 'F') as female_customers
FROM customer AS cu
GROUP BY cu.marital_status;

--- Taux d'endettement moyen par revenue

SELECT income,
       AVG(debt_rate) AS avg_debt_rate
FROM customer
GROUP BY income
ORDER BY income;

--- Répartition des clients par âge

SELECT age,
       COUNT(*) AS count
FROM customer
GROUP BY age;

--- Nombre d'enfants à charge Répartition

SELECT dependent_children,
       COUNT(*) AS count
FROM customer
GROUP BY dependent_children;

--- Composition par sexe

SELECT CASE
           WHEN gender = 'F' THEN 'Femme'
           WHEN gender = 'M' THEN 'Homme'
           ELSE 'Autre'
       END AS gender_format,
       COUNT(*) AS count
FROM customer
GROUP BY gender_format;

--- Revenu moyen par statut marital

SELECT marital_status,
       AVG(income) AS avg_income
FROM customer
GROUP BY marital_status;

