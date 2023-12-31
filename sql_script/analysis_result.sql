CREATE TABLE customer_markting_analysis_data(
    customer_marketing_id INTEGER REFERENCES customer_marketing(id) PRIMARY KEY NOT NULL,
    catalog_car_category_id INTEGER REFERENCES catalog_car_category(id),
    catalog_car_id INTEGER REFERENCES catalog_car(id)
);