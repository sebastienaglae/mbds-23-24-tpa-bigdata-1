from databus import Databus
import pymongo
import pymongo.database

async def treat_car_catalog(db: pymongo.database.Database, databus: Databus):
    # "brand": data["marque"].upper(),
    # "name": data["nom"].upper(),
    # "power": data["puissance"],
    # "length": data["longueur"],
    # "seating_capacity": data["nbPlaces"],
    # "number_doors": data["nbPortes"],
    # "color": data["couleur"],
    # "used": data["occasion"],

    # # other data
    # "price": data["prix"],

    # car_color_mapping = {
    #    "blanc": "white",
    #    "bleu": "blue",
    #    "gris": "grey",
    #    "noir": "black",
    #    "rouge": "red"
    #}
    # longueur_mapping = {
    #    "courte": "short",
    #    "moyenne": "medium",
    #    "longue": "long",
    #    "très longue": "very_long"
    #}
    # regexp_replace("marque", r"Hyunda.", "Hyundai")
    cars = db["catalogue"]
    result = cars.aggregate([
        {
            "$project": {
                "brand": {
                    "$toUpper": {
                        "$switch": {
                            "branches": [
                                {"case": {"$eq": ["$marque", "Hyunda."]}, "then": "Hyundai"}
                            ],
                            "default": "$marque"
                        }
                    }
                },
                "name": {"$toUpper": "$nom"},
                "power": "$puissance",
                "length": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": ["$longueur", "courte"]}, "then": "short"},
                            {"case": {"$eq": ["$longueur", "moyenne"]}, "then": "medium"},
                            {"case": {"$eq": ["$longueur", "longue"]}, "then": "long"},
                            {"case": {"$eq": ["$longueur", "très longue"]}, "then": "very_long"}
                        ],
                        "default": "unknown"
                    }
                },
                "seating_capacity": "$nbPlaces",
                "number_doors": "$nbPortes",
                "color": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": ["$couleur", "blanc"]}, "then": "white"},
                            {"case": {"$eq": ["$couleur", "bleu"]}, "then": "blue"},
                            {"case": {"$eq": ["$couleur", "gris"]}, "then": "grey"},
                            {"case": {"$eq": ["$couleur", "noir"]}, "then": "black"},
                            {"case": {"$eq": ["$couleur", "rouge"]}, "then": "red"}
                        ],
                        "default": "unknown"
                    }
                },
                "used": "$occasion",
                "price": "$prix"
            }
        }
    ])

    def transform_data(data):
        # delete _id
        del data["_id"]
        return data
    
    await databus.publish_result("catalog_car", result, ["brand", "name", "power", "length", "seating_capacity", "number_doors", "color", "used"], transform_data, mode="upsert")
