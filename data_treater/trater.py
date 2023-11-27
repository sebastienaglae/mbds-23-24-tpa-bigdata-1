from pyspark.sql import SparkSession
from cardealer_treater import treat_cardealer
from client_treater import treat_client
from inmatriculation_treater import treat_inmatriculation
from marketing_treater import treat_marketing

def treat_all():
    # Create a SparkSession
    spark = SparkSession.builder.appName("TreaterApplication").getOrCreate()

    # Call the treaters with the SparkSession
   # treat_cardealer(spark)
    treat_client(spark)
   # treat_inmatriculation(spark)
    #treat_marketing(spark)

    # Stop the SparkSession when you're done
    spark.stop()

if __name__ == "__main__":
    treat_all()
