from pyspark.sql import SparkSession
from mongo.catalog_treater import treat_car_catalog as mongo_treat_car_catalog
from redisdb.marketing_treater import treat_marketing as redis_treat_marketing
from spark.cardealer_treater import treat_cardealer
from spark.client_treater import treat_client
from spark.inmatriculation_treater import treat_inmatriculation
from spark.marketing_treater import treat_marketing
from spark.co2_treater import treat_co2

from databus import Databus


import os
import subprocess
import asyncio
import yaml
import redis
import pymongo

async def spark_treat_all(config, databus):
    # Read the configuration file

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
    # await treat_cardealer(spark, general_path, databus) # NOTE: use the mongo_treat_car_catalog
    await treat_inmatriculation(spark, general_path, databus)
    await treat_co2(spark, general_path, databus)
    await treat_client(spark, general_path, databus)
    # await treat_marketing(spark, general_path, databus) # NOTE: use the redis_treat_marketing

    spark.stop()

async def mongodb_treat_all(config, databus):
    client = pymongo.MongoClient(config["mongo"]["connection_string"])
    db = client[config["mongo"]["database"]]

    await mongo_treat_car_catalog(db, databus)

async def redis_treat_all(config, databus):
    r = redis.Redis(host=config["redis"]["host"], port=config["redis"]["port"], db=config["redis"]["db"], password=config["redis"]["password"])
    
    await redis_treat_marketing(r, "Marketing", databus)

async def treat_all(config):
    databus = Databus(config["nats"])
    await databus.connect()

    await spark_treat_all(config, databus)
    await mongodb_treat_all(config, databus)
    await redis_treat_all(config, databus)

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(treat_all(config))
    loop.close()
