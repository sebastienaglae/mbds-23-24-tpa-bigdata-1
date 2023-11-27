from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

def treat_inmatriculation():
    # Initialiser le contexte Spark
    spark = SparkSession.builder.appName("example").getOrCreate()

    # Lire le CSV dans un DataFrame
    immatriculation = spark.read.option("delimiter", ";").csv("C:/Users/vince/Documents/Cours_MBDS/Projet_TPA/TPA_BIGDATA/TPA_BIGDATA/Groupe_TPA_2/M2_DMA_Immatriculations/Immatriculations.csv", header=True)

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

    # Afficher le résultat
    immatriculation.show()

    # Arrêter le contexte Spark
    spark.stop()

# Appeler la fonction pour exécuter le traitement
#treat_inmatriculation()

