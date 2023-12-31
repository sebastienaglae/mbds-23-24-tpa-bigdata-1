import mongodb
import csv
import json

class MongoDriver:
    db = None
    def __init__(self, connection_string, database):
        print("Initializing MongoDB driver with connection string {} and database {}".format(connection_string, database))
        self.db = mongodb.MongoClient(connection_string)[database]


class MongoTarget:
    def __init__(self, driver: MongoDriver, collection):
        self.driver = driver
        self.collection = collection

    def export(self, in_path):
        print("Exporting {} to list {}".format(in_path, self.list_key))
        # if ends with .csv, then use csv reader
        if in_path.endswith('.csv'):
            self.driver.db[self.collection].delete_many({})
            with open(in_path, "r", encoding='utf-8') as reader:
                csv_reader = csv.DictReader(reader)
                for row in csv_reader:
                    json_row = json.dumps(row)
                    print(json_row)
                    # push to mongodb
                    self.driver.db[self.collection].insert_one(row)
        else:
            raise ValueError("Only csv files are supported")