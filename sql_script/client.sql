----------------------------------------------
-- CLIENT TABLE (Client)
----------------------------------------------

-- Table "Client" :
-- age (nombre)
-- sexe (chaîne de caractères)
-- taux (nombre)
-- situationFamiliale (chaîne de caractères)
-- nbEnfantsAcharge (nombre)
-- 2eme voiture (booléen, par exemple True/False)
-- immatriculation (chaîne de caractères)

CREATE TABLE client(
    id SERIAL PRIMARY KEY,
    age NUMERIC,
    gender VARCHAR(255),
    rate NUMERIC,
    marital_status VARCHAR(255),
    dependent_children NUMERIC,
    second_car BOOLEAN,
    registration VARCHAR(255) REFERENCES immatriculation(registration)
)