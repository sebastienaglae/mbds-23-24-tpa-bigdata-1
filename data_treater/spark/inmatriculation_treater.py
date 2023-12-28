from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import regexp_replace, concat_ws
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

from databus import Databus

async def treat_inmatriculation(spark: SparkSession, general_path: str, databus: Databus):
    # Lire le CSV dans un DataFrame
    immatriculation = spark.read.option("delimiter", ",").csv(general_path + "/Immatriculations.csv", header=True)

    # Drop rows with null values
    immatriculation = immatriculation.na.drop()

    # Replace "Hyunda*" (RE) by "Hyundai"
    immatriculation = immatriculation.withColumn("marque", regexp_replace("marque", r"Hyunda.", "Hyundai"))

    # Combine "marque" and "nom" into one column with spark.sql.functions.concat
    immatriculation = immatriculation.withColumn("marque_nom", concat_ws(" ", col("marque"), col("nom")))

    # Encode the column "marque_nom" into "marque_nom_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="marque_nom", outputCol="marque_nom_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(immatriculation)
    immatriculation = model.transform(immatriculation)

    # In the column "longueur" replace "courte" by "1", "moyenne" by "2", "longue" by "3" and "très lon
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"courte", "short"))
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"moyenne", "medium"))
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"très longue", "long"))
    immatriculation = immatriculation.withColumn("longueur", regexp_replace("longueur", r"longue", "very_long"))

    car_color_mapping = {
        "blanc": "white",
        "bleu": "blue",
        "gris": "grey",
        "noir": "black",
        "rouge": "red"
    }
    for key, value in car_color_mapping.items():
        immatriculation = immatriculation.withColumn("couleur", regexp_replace("couleur", key, value))


    # Encode the column "couleur" into "couleur_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="couleur", outputCol="couleur_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(immatriculation)
    immatriculation = model.transform(immatriculation)

    # Convert the columns "longueur", "nbPlaces", "nbPortes" and "puissance" to integer
    immatriculation = immatriculation.withColumn("nbPlaces", immatriculation["nbPlaces"].cast("int"))
    immatriculation = immatriculation.withColumn("nbPortes", immatriculation["nbPortes"].cast("int"))
    immatriculation = immatriculation.withColumn("puissance", immatriculation["puissance"].cast("int"))

    # Convert the column "prix" to float
    immatriculation = immatriculation.withColumn("prix", immatriculation["prix"].cast("float"))
    immatriculation = immatriculation.withColumn("occasion", immatriculation["occasion"].cast("boolean"))

    # Save the DataFrame as csv
    # output_directory = "/home/ernestobone/Documents/M2/TPA/TEST/" + "imm_treated"
    # os.makedirs(output_directory, exist_ok=True)
    # immatriculation.write.csv(output_directory, header=True, mode="overwrite")

    # Send the DF to the DB here
    def transform_data(data):
        return {
            "registration_id": data["immatriculation"],
            "car_id": {
                "from": "catalog_car",
                "pk": "brand,name,power,length,seating_capacity,number_doors,color,used",
                "ref": "id",
                "match": {
                    "brand": data["marque"].upper(),
                    "name": data["nom"].upper(),
                    "power": data["puissance"],
                    "length": data["longueur"],
                    "seating_capacity": data["nbPlaces"],
                    "number_doors": data["nbPortes"],
                    "color": data["couleur"],
                    "used": data["occasion"],

                    "price": data["prix"],
                },
                "allowInsert": True,
                "allowUpdate": True,
            }
        }
    await databus.publish_result("customer_car_registration", [row.asDict() for row in immatriculation.collect()], "registration_id", transform_data)

    print("Immatriculation treated")
    # immatriculation.show()

