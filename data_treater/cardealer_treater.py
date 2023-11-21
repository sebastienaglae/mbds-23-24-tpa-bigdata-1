from pyspark.sql import SparkSession

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace

def treat_cardealer(spark: SparkSession):
    # Read CSV into DataFrame
    cardealer = spark.read.option("delimiter", ";").csv("/user/hduser/cardealer.csv", header=True)

    # Drop rows with null values
    cardealer = cardealer.na.drop()

    # replace "Hyunda*" (RE) by "Hyundai"
    cardealer = cardealer.withColumn("marque", regexp_replace("marque", r"Hyunda\*", "Hyundai"))

    # In the column "longueur" replace "courte" by "1", "moyenne" by "2", "longue" by "3" and "tr\*s longue" by "4"
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"courte", "1"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"moyenne", "2"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"longue", "3"))
    cardealer = cardealer.withColumn("longueur", regexp_replace("longueur", r"tr\*s longue", "4"))

    # Convert the column "longueur", "nbPlaces", "nbPortes" and "puissance" to integer
    cardealer = cardealer.withColumn("longueur", cardealer["longueur"].cast("int"))
    cardealer = cardealer.withColumn("nbPlaces", cardealer["nbPlaces"].cast("int"))
    cardealer = cardealer.withColumn("nbPortes", cardealer["nbPortes"].cast("int"))
    cardealer = cardealer.withColumn("puissance", cardealer["puissance"].cast("int"))

    # Convert the column "prix" to float
    cardealer = cardealer.withColumn("prix", cardealer["prix"].cast("float"))

    # To show the resulting DataFrame
    cardealer.show()
