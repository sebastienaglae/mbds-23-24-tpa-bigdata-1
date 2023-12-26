from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, concat_ws, col
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
import os

def treat_cardealer(spark: SparkSession, general_path: str):
    # Read CSV into DataFrame
    cardealer = spark.read.option("delimiter", ",").csv(general_path + "/Catalogue.csv", header=True, encoding="UTF8")

    # Drop rows with null values
    cardealer = cardealer.na.drop()

    # Replace "Hyunda*" (RE) by "Hyundai"
    cardealer = cardealer.withColumn("marque", regexp_replace("marque", r"Hyunda.", "Hyundai"))

    # Combine "marque" and "nom" into one column with spark.sql.functions.concat
    cardealer = cardealer.withColumn("marque_nom", concat_ws(" ", col("marque"), col("nom")))

    # Drop the columns "marque" and "nom"
    cardealer = cardealer.drop("marque", "nom") # NOTE: Maybe we should keep the column "marque" and "nom" for the data visualization

    # Encode the column "marque_nom" into "marque_nom_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="marque_nom", outputCol="marque_nom_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(cardealer)
    cardealer = model.transform(cardealer)

    # Drop the column "marque_nom"
    cardealer = cardealer.drop("marque_nom")

    # In the column "longueur" replace "courte" by "1", "moyenne" by "2", "longue" by "3" and "très lon
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"courte", "1"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"moyenne", "2"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"très longue", "4"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"longue", "3"))

    # In the column "occasion" replace "true" by "1" and "false" by "0"
    cardealer = cardealer.withColumn("occasion", regexp_replace("occasion", r"true", "1"))
    cardealer = cardealer.withColumn("occasion", regexp_replace("occasion", r"false", "0"))

    # Encode the column "couleur" into "couleur_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="couleur", outputCol="couleur_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(cardealer)
    cardealer = model.transform(cardealer)

    # Drop the column "couleur"
    cardealer = cardealer.drop("couleur") # NOTE: Maybe we should keep the column "couleur" for the data visualization

    # Convert the columns "longueur", "nbPlaces", "nbPortes" and "puissance" to integer
    cardealer = cardealer.withColumn("longueur", cardealer["longueur"].cast("int"))
    cardealer = cardealer.withColumn("nbPlaces", cardealer["nbPlaces"].cast("int"))
    cardealer = cardealer.withColumn("nbPortes", cardealer["nbPortes"].cast("int"))
    cardealer = cardealer.withColumn("puissance", cardealer["puissance"].cast("int"))

    # Convert the column "prix" to float
    cardealer = cardealer.withColumn("prix", cardealer["prix"].cast("float"))

    # Save the DataFrame as csv
    # output_directory = "/home/ernestobone/Documents/M2/TPA/TEST/" + "cardealer_treated"
    # os.makedirs(output_directory, exist_ok=True)
    # cardealer.write.csv(output_directory, header=True, mode="overwrite")

    # Send the DF to the DB here

    # To show the resulting DataFrame
    cardealer.show()
