from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from sklearn.preprocessing import LabelEncoder

def treat_inmatriculation(spark: SparkSession, general_path: str):
    # Lire le CSV dans un DataFrame
    immatriculation = spark.read.option("delimiter", ";").csv(general_path + "/Immatriculations.csv", header=True)

    # Supprimer les lignes avec des valeurs nulles
    immatriculation = immatriculation.na.drop()

    # Transformer les valeurs de la colonne "couleur"
    immatriculation = immatriculation.withColumn(
        "color",
        when(col("_c7") == "gris", "grise")
        .when(col("_c7") == "blanc", "blanche")
        .when(col("_c7") == "bleu", "bleue")
        .otherwise(col("_c7"))
    ).select("_c0", "_c1", "_c2", "_c3", "_c4", "_c5", "_c6", "color", "_c8", "_c9")

    # Supprimer les lignes avec des caractères "?"
    immatriculation = immatriculation.filter(~col("_c0").contains("?") & ~col("_c1").contains("?") & ~col("_c2").contains("?") & ~col("_c3").contains("?") & ~col("_c4").contains("?") & ~col("_c5").contains("?") & ~col("_c6").contains("?") & ~col("color").contains("?") & ~col("_c8").contains("?") & ~col("_c9").contains("?"))

    # combine "marque" and "nom" into one column
    cardealer = cardealer.withColumn("marque_nom", cardealer["marque"] + " " + cardealer["nom"])

    # encode the column "marque_nom" into "marque_nom_encoded"
    label_encoder = LabelEncoder()
    cardealer = cardealer.withColumn("marque_nom_encoded", label_encoder.fit_transform(cardealer["marque_nom"]))
    
    # drop the columns "marque" and "nom"
    cardealer = cardealer.drop("marque", "nom")

    # Afficher le résultat
    immatriculation.show()

