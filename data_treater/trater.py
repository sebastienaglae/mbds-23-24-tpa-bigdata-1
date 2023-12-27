from pyspark.sql import SparkSession
from cardealer_treater import treat_cardealer
from client_treater import treat_client
from databus import Databus
from inmatriculation_treater import treat_inmatriculation
from marketing_treater import treat_marketing
from co2_treater import treat_co2
import os
import subprocess
import asyncio
import yaml

async def treat_all():
    # Read the configuration file
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    databus = Databus(config["nats"])
    await databus.connect()

    # Set HADOOP_USER_NAME environment variable
    os.environ['HADOOP_USER_NAME'] = config["spark"]["hdfsuser"]

    hdfspath = config["spark"]["hdfspath"]

    # Specify the HDFS command you want to run
    hdfs_command = "hdfs dfs -ls " + hdfspath + "/"

    # Execute the command
    subprocess.run(hdfs_command, shell=True)
    # Create a SparkSession
    spark = SparkSession.builder.appName("TreaterApplication").getOrCreate()
    general_path = hdfspath + "/data_wharehouse/"

    # Set HADOOP_USER_NAME environment variable
    spark.conf.set("spark.hadoop.fs.defaultFS", general_path)
    spark.conf.set("spark.hadoop.hadoop.security.username", "root")

    # Call the treaters with the SparkSession
    await treat_cardealer(spark, general_path, databus)
    await treat_inmatriculation(spark, general_path, databus)
    await treat_co2(spark, general_path, databus)
    await treat_client(spark, general_path, databus)
    await treat_marketing(spark, general_path, databus)

    spark.stop()

if __name__ == "__main__":
    task = treat_all()
    asyncio.get_event_loop().run_until_complete(task)
