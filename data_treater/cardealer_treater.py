from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, concat_ws, col
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from databus import Databus

async def treat_cardealer(spark: SparkSession, general_path: str, databus: Databus):
    # Read CSV into DataFrame
    cardealer = spark.read.option("delimiter", ",").csv(general_path + "/Catalogue.csv", header=True, encoding="UTF8")

    # Drop rows with null values
    cardealer = cardealer.na.drop()

    # Replace "Hyunda*" (RE) by "Hyundai"
    cardealer = cardealer.withColumn("marque", regexp_replace("marque", r"Hyunda.", "Hyundai"))

    # Combine "marque" and "nom" into one column with spark.sql.functions.concat
    cardealer = cardealer.withColumn("marque_nom", concat_ws(" ", col("marque"), col("nom")))

    # Drop the columns "marque" and "nom"
    # cardealer = cardealer.drop("marque", "nom") # NOTE: Maybe we should keep the column "marque" and "nom" for the data visualization

    # Encode the column "marque_nom" into "marque_nom_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="marque_nom", outputCol="marque_nom_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(cardealer)
    cardealer = model.transform(cardealer)

    # Drop the column "marque_nom"
    cardealer = cardealer.drop("marque_nom")

    # In the column "longueur" replace "courte" by "1", "moyenne" by "2", "longue" by "3" and "très lon
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"courte", "short"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"moyenne", "medium"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"très longue", "long"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"longue", "very_long"))

    # In the column "occasion" replace "true" by "1" and "false" by "0"
    # cardealer = cardealer.withColumn("occasion", regexp_replace("occasion", r"true", "1"))
    # cardealer = cardealer.withColumn("occasion", regexp_replace("occasion", r"false", "0"))

    # Encode the column "couleur" into "couleur_encoded" using StringIndexer
    string_indexer = StringIndexer(inputCol="couleur", outputCol="couleur_encoded", handleInvalid="skip")
    pipeline = Pipeline(stages=[string_indexer])
    model = pipeline.fit(cardealer)
    cardealer = model.transform(cardealer)

    # Change couleur from blanc, bleu, gris, noir, rouge to white, blue, grey, black, red    
    car_color_mapping = {
        "blanc": "white",
        "bleu": "blue",
        "gris": "grey",
        "noir": "black",
        "rouge": "red"
    }
    for key, value in car_color_mapping.items():
        cardealer = cardealer.withColumn("couleur", regexp_replace("couleur", key, value))

    # Drop the column "couleur"
    # cardealer = cardealer.drop("couleur") # NOTE: Maybe we should keep the column "couleur" for the data visualization

    # Convert the columns "longueur", "nbPlaces", "nbPortes" and "puissance" to integer
    cardealer = cardealer.withColumn("nbPlaces", cardealer["nbPlaces"].cast("int"))
    cardealer = cardealer.withColumn("nbPortes", cardealer["nbPortes"].cast("int"))
    cardealer = cardealer.withColumn("puissance", cardealer["puissance"].cast("int"))

    # Convert the column "prix" to float
    cardealer = cardealer.withColumn("prix", cardealer["prix"].cast("float"))

    # Save the DataFrame as csv
    # output_directory = "/home/ernestobone/Documents/M2/TPA/TEST/" + "cardealer_treated"
    # os.makedirs(output_directory, exist_ok=True)
    # cardealer.write.csv(output_directory, header=True, mode="overwrite")
    def transform_data(data):
        if data["longueur"] not in ["short", "medium", "long", "very_long"]:
            raise Exception(data["longueur"])
        if data["couleur"] not in ["white", "blue", "grey", "black", "red"]:
            raise Exception(data["couleur"])

        return {
            # key attributes
            "brand": data["marque"].upper(),
            "name": data["nom"].upper(),
            "power": data["puissance"],
            "length": data["longueur"],
            "seating_capacity": data["nbPlaces"],
            "number_doors": data["nbPortes"],
            "color": data["couleur"],
            "used": data["occasion"],

            # other data
            "price": data["prix"],
        }
    
    await databus.publish_result("catalog_car", cardealer.collect(), ["brand", "name", "power", "length", "seating_capacity", "number_doors", "color", "used"], transform_data, mode="upsert")
    
    cardealer.show()
