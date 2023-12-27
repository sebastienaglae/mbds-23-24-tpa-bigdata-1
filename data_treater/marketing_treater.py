from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace
from databus import Databus

async def treat_marketing(sc: SparkSession, general_path: str, databus: Databus):
            
    marketing = sc.read.option("delimiter", ",").csv(general_path + "/Marketing.csv", header=True, encoding="UTF8")

    marketing = marketing.na.drop()

    marketing = marketing.filter((marketing.situationFamiliale != "") & (marketing.situationFamiliale != "?") & (marketing.situationFamiliale != "è") & (marketing.situationFamiliale != " ") & (marketing.situationFamiliale != "N/D"))
    marketing = marketing.filter((marketing.sexe != "") & (marketing.sexe != "?") & (marketing.sexe != "è") & (marketing.sexe != " ") & (marketing.sexe != "N/D"))
    marketing = marketing.filter((marketing["2eme voiture"] != "") & (marketing["2eme voiture"] != "?"))
    marketing = marketing.filter((marketing["taux"] != "") & (marketing["taux"] != "?") & (marketing["taux"] != " ") & (marketing["taux"] != "-1"))
    marketing = marketing.filter((marketing["nbEnfantsAcharge"] != "") & (marketing["nbEnfantsAcharge"] != "?") & (marketing["nbEnfantsAcharge"] != " ") & (marketing["nbEnfantsAcharge"] != "-1"))
    marketing = marketing.filter((marketing["age"] != "") & (marketing["age"] != "?") & (marketing["age"] != " ") & (marketing["age"] != "-1"))

    marital_status_mapping = {
        r"C.libataire": "single",
        r"Divorc.e": "divorced",
        r"En Couple": "couple",
        r"Mari.+": "married",
        r"Seule": "single",
        r"Seul": "single",
    }
    for key, value in marital_status_mapping.items():
        marketing = marketing.withColumn("situationFamiliale", regexp_replace("situationFamiliale", key, value))

    marketing = marketing.withColumn("2eme voiture", marketing["2eme voiture"].cast("boolean"))

    # output_directory = "/home/ernestobone/Documents/M2/TPA/" + "marketing_treated"
    # os.makedirs(output_directory, exist_ok=True)
    # marketing.write.csv(output_directory, header=True, mode="overwrite")

    def transform_data(data):
        if data["situationFamiliale"] not in ["single", "couple", "married", "divorced", "widowed"]:
            raise Exception("Unknown marital status: " + data["situationFamiliale"])
        if data["sexe"] not in ["F", "M"]:
            raise Exception("Unknown sex: " + data["sexe"])

        return {
            # key attributes
            "age": data["age"],
            "gender": data["sexe"],
            "debt_rate": data["taux"],
            "marital_status": data["situationFamiliale"],
            "dependent_children": data["nbEnfantsAcharge"],
            "has_second_car": data["2eme voiture"]
        }
    
    await databus.publish_result("customer_marketing", marketing.collect(), ["age", "gender", "debt_rate", "marital_status", "dependent_children", "has_second_car"], transform_data, mode="upsert")

    marketing.show()