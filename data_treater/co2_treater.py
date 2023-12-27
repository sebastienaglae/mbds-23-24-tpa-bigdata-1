from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace

def treat_co2(spark: SparkSession, general_path: str):
    # Lire le CSV dans un DataFrame
    co2 = spark.read.option("delimiter", ",").csv(general_path + "/CO2.csv", header=True)

    # Drop rows with null values
    co2 = co2.na.drop()

    # Drop the first column, which is useless
    co2 = co2.drop("_c0")

    # For the column 'Bonus / Malus' remove every character after the € sign (keep all the characters before the € sign)
    co2 = co2.withColumn("Bonus / Malus", regexp_replace("Bonus / Malus", r"€.*", "")) 

    # For the column 'Cout enerie' replace the header 'Cout enerie' by 'Cout energie'
    co2 = co2.withColumnRenamed("Cout enerie", "Cout energie")

    #for the column 'Cout energie' remove every character after the € sign (keep all the characters before the € sign)
    co2 = co2.withColumn("Cout energie", regexp_replace("Cout energie", r"€.*", ""))

    # Create a new column 'Marque' from 'Marque / Modele' keeping everything before the space
    co2 = co2.withColumn("Marque", regexp_replace("Marque / Modele", r" .*", ""))

    # For the column 'Marque / Modele' keep the match of the group 1 from this regex [A-Z]+\s(.+) (keep everything after the space)
    co2 = co2.withColumn("Modele", regexp_replace("Marque / Modele", r"[A-Z]+\s(.+)", "$1"))

    # Remove the comlumn 'Marque / Modele'
    co2 = co2.drop("Marque / Modele")

    # Save the DataFrame into the DB here


    co2.show()