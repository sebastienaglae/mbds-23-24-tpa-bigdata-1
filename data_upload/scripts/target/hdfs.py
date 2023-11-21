from hdfs import InsecureClient

class HdfsDriver:
    def __init__(self, url):
        print("Initializing HDFS driver with url {}".format(url))
        self.client = InsecureClient(url)
    def write(self, path, data):
        with self.client.write(path, encoding="utf-8") as writer:
            writer.write(data)

class HdfsTarget:
    def __init__(self, driver, path):
        self.driver = driver
        self.path = path

    def export(self, in_path):
        print("Exporting {} to {}".format(in_path, self.path))
        with open(in_path, "r") as reader:
            data = reader.read()
            self.driver.write(self.path, data)