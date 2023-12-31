import redis
import csv
import json

class RedisDriver:
    client = redis.Redis
    def __init__(self, host, port, password, db):
        print("Initializing Redis driver with host {} and port {}".format(host, port))
        self.client = redis.Redis(host=host, port=port, password=password, db=db)

class RedisTarget:
    def __init__(self, driver: RedisDriver, list_key):
        self.driver = driver
        self.list_key = list_key

    def export(self, in_path):
        print("Exporting {} to list {}".format(in_path, self.list_key))
        # if ends with .csv, then use csv reader
        if in_path.endswith('.csv'):
            # drop all data in the list
            self.driver.client.delete(self.list_key)
            with open(in_path, "r", encoding='utf-8') as reader:
                csv_reader = csv.DictReader(reader)
                for row in csv_reader:
                    # export to redis in json format
                    json_row = json.dumps(row)
                    print(json_row)
                    self.driver.client.rpush(self.list_key, json_row)
        else:
            with open(in_path, "r") as reader:
                data = reader.read()
                self.driver.client.rpush(self.list_key, data)