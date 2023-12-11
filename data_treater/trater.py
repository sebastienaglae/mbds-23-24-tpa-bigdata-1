from pyspark.sql import SparkSession
from cardealer_treater import treat_cardealer
from client_treater import treat_client
from inmatriculation_treater import treat_inmatriculation
from marketing_treater import treat_marketing

def treat_all():
    # Create a SparkSession
    spark = SparkSession.builder.appName("TreaterApplication").getOrCreate()
    general_path = "/home/ernestobone/Documents/M2/TPA/OneDrive_1_15-11-2023/"

    # Call the treaters with the SparkSession
    treat_cardealer(spark, general_path + "M2_DMA_Catalogue/")
    # treat_client(spark, general_path)
    # treat_inmatriculation(spark, general_path)
    treat_marketing(spark, general_path + "M2_DMA_Marketing/")

    # Stop the SparkSession when you're done
    spark.stop()

if __name__ == "__main__":
    treat_all()
