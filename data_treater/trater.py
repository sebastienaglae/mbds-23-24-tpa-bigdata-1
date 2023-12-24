from pyspark.sql import SparkSession
from cardealer_treater import treat_cardealer
from client_treater import treat_client
from inmatriculation_treater import treat_inmatriculation
from marketing_treater import treat_marketing
import os
import subprocess

def treat_all():


    # Set HADOOP_USER_NAME environment variable
    os.environ['HADOOP_USER_NAME'] = 'root'

    # Specify the HDFS command you want to run
    hdfs_command = "hdfs dfs -ls /"  # Replace with your desired HDFS command

    # Execute the command
    subprocess.run(hdfs_command, shell=True)
    # Create a SparkSession
    spark = SparkSession.builder.appName("TreaterApplication").getOrCreate()
    general_path = "hdfs://135.181.84.87:9000/data_wharehouse/"

    # Set HADOOP_USER_NAME environment variable
    spark.conf.set("spark.hadoop.fs.defaultFS", general_path)
    spark.conf.set("spark.hadoop.hadoop.security.username", "root")

    # Call the treaters with the SparkSession
    treat_cardealer(spark, general_path)
    # treat_client(spark, general_path)
    # treat_inmatriculation(spark, general_path)
    treat_marketing(spark, general_path)

    # Stop the SparkSession when you're done
    spark.stop()

if __name__ == "__main__":
    treat_all()
