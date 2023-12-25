from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace

def treat_client(spark: SparkSession, general_path: str):

    # Lire le CSV dans un DataFrame
    data11 = spark.read.option("delimiter", ",").csv(general_path + "/Clients_11.csv", header=True)
    columns11 = ["age", "sexe", "taux", "situationFamiliale", "nbEnfantsAcharge", "2eme voiture", "immatriculation"]
    client11 = spark.createDataFrame(data11.rdd, columns11)

    data19 = spark.read.option("delimiter", ",").csv(general_path + "/Clients_19.csv", header=True)
    columns19 = ["age", "sexe", "taux", "situationFamiliale", "nbEnfantsAcharge", "2eme voiture", "immatriculation"]
    client19 = spark.createDataFrame(data19.rdd, columns19)

    # Concaténer les deux DataFrames
    client = client11.union(client19)

    # compare client11 schema with client schema, if they are different, then print the schema
    if client11.schema != client.schema:
        print(client.schema)
        print("Not the same schema")

    client = client.na.drop()

    client = client.withColumn("situationFamiliale", regexp_replace("situationFamiliale", r"C.libataire", "1"))
    client = client.withColumn("situationFamiliale", regexp_replace("situationFamiliale", r"Seule", "1"))
    client = client.withColumn("situationFamiliale", regexp_replace("situationFamiliale", r"En Couple", "2"))

    client = client.withColumn("2eme voiture", regexp_replace("2eme voiture", r"true", "1"))
    client = client.withColumn("2eme voiture", regexp_replace("2eme voiture", r"false", "0"))

    client = client.withColumn("sexe", regexp_replace("sexe", r"F", "0"))
    client = client.withColumn("sexe", regexp_replace("sexe", r"M", "1"))

    client.show()


