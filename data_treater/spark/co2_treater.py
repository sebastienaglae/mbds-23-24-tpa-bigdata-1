from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, replace

from databus import Databus

async def treat_co2(spark: SparkSession, general_path: str, databus: Databus):
    # Lire le CSV dans un DataFrame
    co2 = spark.read.option("delimiter", ",").csv(general_path + "/CO2.csv", header=True)

    # Drop rows with null values
    co2 = co2.na.drop()

    # Drop the first column, which is useless
    co2 = co2.drop("_c0")

    co2 = co2.withColumnRenamed("Cout enerie", "Cout energie")

    # For the column 'Bonus / Malus' remove every character after the € sign (keep all the characters before the € sign)
    replace_map = {
        r"€.*": "",
        r"€": "",
        r"^-$": "0",
        r"\xc2": "",
        r"\xa0": "",
        r"\x20": "",
        r" ": "",
        r"\"": "",
    }
    for key, value in replace_map.items():
        co2 = co2.withColumn("Bonus / Malus", regexp_replace("Bonus / Malus", key, value))
        co2 = co2.withColumn("Cout energie", regexp_replace("Cout energie", key, value))

    # Create a new column 'Marque' from 'Marque / Modele' keeping everything before the space
    co2 = co2.withColumn("Marque", regexp_replace("Marque / Modele", r" .*", ""))
    co2 = co2.withColumn("Marque", regexp_replace("Marque", r"\"", ""))

    # For the column 'Marque / Modele' keep the match of the group 1 from this regex [A-Z]+\s(.+) (keep everything after the space)
    co2 = co2.withColumn("Modele", regexp_replace("Marque / Modele", r"[A-Z]+\s(.+)", "$1"))
    co2 = co2.withColumn("Modele", regexp_replace("Modele", r"\"", ""))

    # Remove the comlumn 'Marque / Modele'
    co2 = co2.drop("Marque / Modele")

    # Convert the column to float
    co2 = co2.withColumn("Rejets CO2 g/km", co2["Rejets CO2 g/km"].cast("float"))
    co2 = co2.withColumn("Bonus / Malus", co2["Bonus / Malus"].cast("float"))
    co2 = co2.withColumn("Cout energie", co2["Cout energie"].cast("float"))

    # Save the DataFrame into the DB here
    def transform_data(data):
        return {
            # key attributes
            "brand": data["Marque"].upper(),
            "car_name": data["Modele"].upper(),
            "bonus_malus": data["Bonus / Malus"],
            "co2_emissions": data["Rejets CO2 g/km"],
            "energy_cost": data["Cout energie"],
        }
    
    await databus.publish_result("brand_co2_emissions", [row.asDict() for row in co2.collect()], ["brand", "car_name"], transform_data, mode="upsert")

    co2.show()