from pyspark.sql import SparkSession

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace

def treat_marketing(sc: SparkSession, general_path: str):
            
    marketing = sc.read.option("delimiter", ",").csv(general_path + "/Marketing.csv", header=True, encoding="UTF8")

    marketing = marketing.na.drop()

    marketing = marketing.withColumn("situationFamiliale", regexp_replace("situationFamiliale", r"C.libataire", "1"))
    marketing = marketing.withColumn("situationFamiliale", regexp_replace("situationFamiliale", r"En Couple", "2"))

    marketing = marketing.withColumn("2eme voiture", regexp_replace("2eme voiture", r"true", "1"))
    marketing = marketing.withColumn("2eme voiture", regexp_replace("2eme voiture", r"false", "0"))

    marketing = marketing.withColumn("sexe", regexp_replace("sexe", r"F", "0"))
    marketing = marketing.withColumn("sexe", regexp_replace("sexe", r"M", "1"))
    
    marketing.write.csv("/home/ernestobone/Documents/M2/TPA" + "/Marketing_treated", header=True, mode="overwrite")

    marketing.show()