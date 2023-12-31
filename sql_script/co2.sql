CREATE TABLE brand_co2_emissions (
    brand VARCHAR(32) NOT NULL,
    car_name VARCHAR(255) NOT NULL,

    bonus_malus NUMERIC CHECK (bonus_malus >= -15000 AND bonus_malus <= 15000),
    co2_emissions NUMERIC CHECK (co2_emissions >= 0 AND co2_emissions <= 500),
    energy_cost NUMERIC CHECK (energy_cost >= 0 AND energy_cost <= 2000),

    PRIMARY KEY (brand, car_name)
);

CREATE VIEW brand_co2_average AS
    SELECT brand, AVG(co2_emissions) AS average_co2_emissions, AVG(energy_cost) AS average_energy_cost, AVG(bonus_malus) AS average_bonus_malus
    FROM brand_co2_emissions
    GROUP BY brand;

-- trigger to update catalog_car data when inserting a new car
CREATE FUNCTION update_catalog_car_co2_emissions()
    RETURNS TRIGGER AS $$
    BEGIN
        -- average values for the brand
        NEW.bonus_malus = (SELECT average_bonus_malus FROM brand_co2_average WHERE brand = NEW.brand);
        NEW.co2_emissions = (SELECT average_co2_emissions FROM brand_co2_average WHERE brand = NEW.brand);
        NEW.energy_cost = (SELECT average_energy_cost FROM brand_co2_average WHERE brand = NEW.brand);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
CREATE TRIGGER update_catalog_car_co2_emissions
    BEFORE INSERT OR UPDATE ON catalog_car
    FOR EACH ROW
    EXECUTE PROCEDURE update_catalog_car_co2_emissions();

-- trigger to update rows in catalog_car when inserting a new row in brand_co2_emissions
CREATE FUNCTION update_catalog_car_co2_emissions_from_brand_co2_emissions()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE catalog_car
        SET bonus_malus = (SELECT average_bonus_malus FROM brand_co2_average WHERE brand = NEW.brand),
            co2_emissions = (SELECT average_co2_emissions FROM brand_co2_average WHERE brand = NEW.brand),
            energy_cost = (SELECT average_energy_cost FROM brand_co2_average WHERE brand = NEW.brand)
        WHERE brand = NEW.brand;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
CREATE TRIGGER update_catalog_car_co2_emissions_from_brand_co2_emissions
    AFTER INSERT OR UPDATE ON brand_co2_emissions
    FOR EACH ROW
    EXECUTE PROCEDURE update_catalog_car_co2_emissions_from_brand_co2_emissions();