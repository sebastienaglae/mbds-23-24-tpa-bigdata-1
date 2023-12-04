import subprocess

class HdfsDriver:
    def __init__(self, url):
        print("Initializing HDFS driver with url {}".format(url))
        self.url = url
    def write(self, path, data):
        proc = subprocess.Popen(["hdfs", "dfs", "-put", '-f', "-", self.url + path],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        comm = proc.communicate(input=data.encode("utf-8"))
        proc.wait()
        if proc.returncode != 0:
            raise Exception("Error exporting to HDFS: {}".format(comm[1]))
        print("Exported {} to {}".format(path, self.url))

class HdfsTarget:
    def __init__(self, driver, path):
        self.driver = driver
        self.path = path

    def export(self, in_path):
        print("Exporting {} to {}".format(in_path, self.path))
        with open(in_path, "r") as reader:
            data = reader.read()
            self.driver.write(self.path, data)
            