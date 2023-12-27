----------------------------------------------
-- IMMATRICULATION TABLE (Immatriculation)
----------------------------------------------

-- Table "Immatriculation" :
-- immatriculation (chaîne de caractères)
-- marque (chaîne de caractères)
-- nom (chaîne de caractères)
-- puissance (nombre)
-- longueur (nombre)
-- nbPlaces (nombre)
-- nbPortes (nombre)
-- couleur (chaîne de caractères)
-- occasion (booléen, par exemple True/False)
-- prix (nombre)

CREATE TABLE immatriculation (
    registration VARCHAR(255) PRIMARY KEY,
    brand VARCHAR(255),
    immat_name VARCHAR(255),
    power NUMERIC,
    immat_length NUMERIC,
    seating_capacity NUMERIC,
    number_doors NUMERIC,
    color VARCHAR(255),
    used BOOLEAN,
    price NUMERIC
);
