from databus import Databus
import json
import redis
import re

def is_valid_row(row):
    # for each row, check if it is valid
    for key, value in row.items():
        if value == "" or value == "?" or value == "è" or value == " " or value == "N/D":
            return False
        
    return True
def apply_mapping(row, mapping):
    for regex, replacement in mapping.items():
        row = re.sub(regex, replacement, row)
    return row

async def treat_marketing(db: redis.Redis, list_name, databus: Databus):
    pos = 0
    len = db.llen(list_name)
    while pos < len:
        data = db.lrange(list_name, pos, pos + 1000)
        pos += 1000

        data = [json.loads(d) for d in data]
        data = [row for row in data if is_valid_row(row)]

        marital_status_mapping = {
            r"C.libataire": "single",
            r"Divorc.e": "divorced",
            r"En Couple": "couple",
            r"Mari.+": "married",
            r"Seule": "single",
            r"Seul": "single",
        }
        genre_mapping = {
            r"Masculin": "M",
            r"F.minin": "F",
            r"Homme": "M",
            r"Femme": "F",
        }

        for row in data:
            row["situationFamiliale"] = apply_mapping(row["situationFamiliale"], marital_status_mapping)
            row["sexe"] = apply_mapping(row["sexe"], genre_mapping)

            row["2eme voiture"] = row["2eme voiture"].lower() == "true"
            row["taux"] = float(row["taux"])
            row["nbEnfantsAcharge"] = int(row["nbEnfantsAcharge"])
            row["age"] = int(row["age"])

        def transform_data(data):
            if data["situationFamiliale"] not in ["single", "couple", "married", "divorced", "widowed"]:
                raise Exception("Unknown marital status: " + data["situationFamiliale"])
            if data["sexe"] not in ["F", "M"]:
                raise Exception("Unknown sex: " + data["sexe"])
            
            assert data["age"] >= 18
            assert data["nbEnfantsAcharge"] >= 0

            return {
                # key attributes
                "age": data["age"],
                "gender": data["sexe"],
                "debt_rate": data["taux"],
                "marital_status": data["situationFamiliale"],
                "dependent_children": data["nbEnfantsAcharge"],
                "has_second_car": data["2eme voiture"]
            }
        
        await databus.publish_result("customer_marketing", data, ["age", "gender", "debt_rate", "marital_status", "dependent_children", "has_second_car"], transform_data, mode="upsert")