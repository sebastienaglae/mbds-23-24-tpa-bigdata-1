import os
import sys
import argparse

from pyspark.sql import SparkSession

# Marque / Modele	Bonus / Malus	Rejets CO2 g/km	Cout enerie
ATTEMPTED_CSV_HEADER = ["Marque / Modele", "Bonus / Malus", "Rejets CO2 g/km", "Cout enerie"]

def parse_currency(value):
    if len(value) < 1 or (len(value) == 1 and value[0] == '-'):
        return 0
    
    currency_sign = value[0]
    currency_symbol = value.index('€')
    if currency_symbol == -1:
        raise ValueError("Expected currency symbol € not found in {}".format(value))
    if currency_sign not in ['+', '-']:
        # check if number else raise ValueError
        if not currency_sign.isdigit():
            raise ValueError("Expected currency sign + or - not found in {}".format(value))
    
    currency_value = value[1:currency_symbol] if not currency_sign.isdigit() else value[currency_symbol]
    
    sign = 1 if currency_sign == '+' else -1
    number = currency_value.replace(' ', '')

    return sign * int(number)

class ProductInfo:
    def __init__(self, model, bonus, co2PerKm, energyCost):
        self.model = model
        self.bonus = -parse_currency(bonus)
        self.co2PerKm = co2PerKm
        self.energyCost = parse_currency(energyCost)
    
    def __str__(self):
        return "ProductInfo(model={}, bonus={}, co2PerKm={}, energyCost={})".format(self.model, self.bonus, self.co2PerKm, self.energyCost)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Path to the input file", required=True)
    
    args = parser.parse_args()
    input_path = args.input

    # init SparkSession
    spark = SparkSession.builder.master("local[2]").appName("CO2 Emission").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # read csv file
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # check if header matches
    header = df.schema.names
    if header != ATTEMPTED_CSV_HEADER:
        print("Header from csv file does not match the expected header: {}".format(ATTEMPTED_CSV_HEADER))
        sys.exit(1)

    # load products
    products = df.rdd.map(lambda row: ProductInfo(row[0], row[1], row[2], row[3]))
    print("Products loaded: {}".format(products.count()))

    