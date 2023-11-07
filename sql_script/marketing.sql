----------------------------------------------
-- MARKETING TABLE (Marketing)
----------------------------------------------

-- Table "Marketing" :
-- age (nombre)
-- sexe (chaîne de caractères)
-- taux (nombre)
-- situationFamiliale (chaîne de caractères)
-- nbEnfantsAcharge (nombre)
-- 2eme voiture (booléen, par exemple True/False)

CREATE TABLE marketing (
    id SERIAL PRIMARY KEY,
    age NUMERIC,
    gender VARCHAR(255),
    rate NUMERIC,
    marital_status VARCHAR(255),
    dependent_children NUMERIC,
    second_car BOOLEAN
);