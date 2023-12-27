from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace
from databus import Databus

async def treat_client(spark: SparkSession, general_path: str, databus: Databus):

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

    # skip data with ? as situationFamiliale
    client = client.filter((client.situationFamiliale != "") & (client.situationFamiliale != "?") & (client.situationFamiliale != "è") & (client.situationFamiliale != " ") & (client.situationFamiliale != "N/D"))
    client = client.filter((client.sexe != "") & (client.sexe != "?") & (client.sexe != "è") & (client.sexe != " ") & (client.sexe != "N/D"))
    client = client.filter((client["2eme voiture"] != "") & (client["2eme voiture"] != "?"))
    client = client.filter((client["taux"] != "") & (client["taux"] != "?") & (client["taux"] != " ") & (client["taux"] != "-1"))
    client = client.filter((client["nbEnfantsAcharge"] != "") & (client["nbEnfantsAcharge"] != "?") & (client["nbEnfantsAcharge"] != " ") & (client["nbEnfantsAcharge"] != "-1"))
    client = client.filter((client["age"] != "") & (client["age"] != "?") & (client["age"] != " ") & (client["age"] != "-1"))

    # change Célibataire, Divorcée, En Couple, Marié(e), Seul, Seule to 'single', 'married', 'divorced', 'widowed'
    marital_status_mapping = {
        r"C.libataire": "single",
        r"Divorc.e": "divorced",
        r"En Couple": "couple",
        r"Mari.+": "married",
        r"Seule": "single",
        r"Seul": "single",
    }
    for key, value in marital_status_mapping.items():
        client = client.withColumn("situationFamiliale", regexp_replace("situationFamiliale", key, value))

    #client = client.withColumn("2eme voiture", regexp_replace("2eme voiture", r"true", "1"))
    #client = client.withColumn("2eme voiture", regexp_replace("2eme voiture", r"false", "0"))

    client = client.withColumn("sexe", regexp_replace("sexe", r"Masculin", "M"))
    client = client.withColumn("sexe", regexp_replace("sexe", r"F.minin", "F"))
    client = client.withColumn("sexe", regexp_replace("sexe", r"Homme", "M"))
    client = client.withColumn("sexe", regexp_replace("sexe", r"Femme", "F"))

    # map 2eme voiture to boolean
    client = client.withColumn("2eme voiture", client["2eme voiture"].cast("boolean"))
    client = client.withColumn("taux", client["taux"].cast("float"))
    client = client.withColumn("nbEnfantsAcharge", client["nbEnfantsAcharge"].cast("int"))
    client = client.withColumn("age", client["age"].cast("int"))


    # output_directory = "/home/ernestobone/Documents/M2/TPA/TEST/" + "client_treated"
    # os.makedirs(output_directory, exist_ok=True)
    # client.write.csv(output_directory, header=True, mode="overwrite")

    # age NUMERIC CHECK (age >= 18),
    # gender customer_gender,
    # debt_rate NUMERIC CHECK (debt_rate >= 0),
    # income NUMERIC GENERATED ALWAYS AS (ROUND(debt_rate / 0.3, 2)) STORED,
    # marital_status customer_marital_status,
    # dependent_children NUMERIC CHECK (dependent_children >= 0),
    # has_second_car BOOLEAN,
    def transform_data(data):
        if data["situationFamiliale"] not in ["single", "couple", "married", "divorced", "widowed"]:
            raise Exception("Unknown marital status: " + data["situationFamiliale"] + " " + data["immatriculation"])
        if data["sexe"] not in ["F", "M"]:
            raise Exception("Unknown sex: " + data["sexe"])

        return {
            # key attributes
            "age": data["age"],
            "gender": data["sexe"],
            "debt_rate": data["taux"],
            "marital_status": data["situationFamiliale"],
            "dependent_children": data["nbEnfantsAcharge"],
            "has_second_car": data["2eme voiture"],
            "current_registration_id": data["immatriculation"].upper(),
        }
    
    await databus.publish_result("customer", client.collect(), ["age", "gender", "debt_rate", "marital_status", "dependent_children", "has_second_car"], transform_data, mode="upsert")

    # Send the DF to the DB here

    client.show()


