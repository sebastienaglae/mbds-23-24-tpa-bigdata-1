from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import regexp_replace, concat_ws
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
import os


def treat_inmatriculation(spark: SparkSession, general_path: str):
    # Lire le CSV dans un DataFrame
    immatriculation = spark.read.option("delimiter", ",").csv(general_path + "/Immatriculations.csv", header=True)

    # Drop rows with null values
    immatriculation = immatriculation.na.drop()

    # Replace "Hyunda*" (RE) by "Hyundai"
    immatriculation = immatriculation.withColumn("marque", regexp_replace("marque", r"Hyunda.", "Hyundai"))

    # Combine "marque" and "nom" into one column with spark.sql.functions.concat
    immatriculation = immatriculation.withColumn("marque_nom", concat_ws(" ", col("marque"), col("nom")))

    # Drop the columns "marque" and "nom"
    immatriculation = immatriculation.drop("marque", "nom") # NOTE: Maybe we should keep the column "marque" and "nom" for the data visualization

    # Encode the column "marque_nom" into "marque_nom_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="marque_nom", outputCol="marque_nom_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(immatriculation)
    immatriculation = model.transform(immatriculation)

    # Drop the column "marque_nom"
    immatriculation = immatriculation.drop("marque_nom")

    # In the column "longueur" replace "courte" by "1", "moyenne" by "2", "longue" by "3" and "très lon
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"courte", "1"))
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"moyenne", "2"))
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"très longue", "4"))
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"longue", "3"))

    # In the column "occasion" replace "true" by "1" and "false" by "0"
    immatriculation = immatriculation.withColumn("occasion", regexp_replace("occasion", r"true", "1"))
    immatriculation = immatriculation.withColumn("occasion", regexp_replace("occasion", r"false", "0"))

    # Encode the column "couleur" into "couleur_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="couleur", outputCol="couleur_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(immatriculation)
    immatriculation = model.transform(immatriculation)

    # Drop the column "couleur"
    immatriculation = immatriculation.drop("couleur") # NOTE: Maybe we should keep the column "couleur" for the data visualization

    # Convert the columns "longueur", "nbPlaces", "nbPortes" and "puissance" to integer
    immatriculation = immatriculation.withColumn("longueur", immatriculation["longueur"].cast("int"))
    immatriculation = immatriculation.withColumn("nbPlaces", immatriculation["nbPlaces"].cast("int"))
    immatriculation = immatriculation.withColumn("nbPortes", immatriculation["nbPortes"].cast("int"))
    immatriculation = immatriculation.withColumn("puissance", immatriculation["puissance"].cast("int"))

    # Convert the column "prix" to float
    immatriculation = immatriculation.withColumn("prix", immatriculation["prix"].cast("float"))

    # Save the DataFrame as csv
    # output_directory = "/home/ernestobone/Documents/M2/TPA/TEST/" + "imm_treated"
    # os.makedirs(output_directory, exist_ok=True)
    # immatriculation.write.csv(output_directory, header=True, mode="overwrite")

    # Send the DF to the DB here
    
    immatriculation.show()

