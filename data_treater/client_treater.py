from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

def treat_client():
    # Initialiser le contexte Spark
    spark = SparkSession.builder.appName("example").getOrCreate()

    # Lire le CSV dans un DataFrame
    client = spark.read.option("delimiter", ";").csv("C:/Users/vince/Documents/Cours_MBDS/Projet_TPA/TPA_BIGDATA/TPA_BIGDATA/Groupe_TPA_2/M2_DMA_Clients_12/Clients_11.csv", header=True)

    # Transformer les valeurs de la colonne "sexe"
    client = client.withColumn(
        "gender", 
        when(col("_c1").isin(["Homme", "H", "Masculin"]), "Homme").otherwise("Femme")
    ).select("_c0", "gender", "_c2", "_c3", "_c4", "_c5", "_c6")

    # Effacer les lignes avec des éléments NaN dans toutes les colonnes du fichier client
    client = client.na.drop()

    # Effacer les lignes ayant des caractères "?" dans toutes les colonnes du fichier client
    client = client.filter(~col("_c0").contains("?") & ~col("gender").contains("?") & ~col("_c2").contains("?") & ~col("_c3").contains("?") & ~col("_c4").contains("?") & ~col("_c5").contains("?") & ~col("_c6").contains("?"))

    # Remplacer les éléments "Seul" et "Seule" par "Celibataire" et "Marie(e)" par "En couple". On conserve uniquement "En couple" et "Célibataire"
    client = client.withColumn(
        "marital_status",
        when(col("_c3").isin(["Célibataire"]), "Célibataire").otherwise("En couple")
    ).select("_c0", "gender", "_c2", "marital_status", "_c4", "_c5", "_c6")

    # Afficher le client résultant
    client.show()

    # Arrêter le contexte Spark
    spark.stop()
    
    # Appeler la fonction pour exécuter le traitement
    treat_client()

