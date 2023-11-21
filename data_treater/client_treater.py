from pyspark import SparkContext

def treat_client(sc: SparkContext):
    
    client = sc.textFile("/user/hduser/client.csv")
    # Split each line of the csv files by the delimiter ";"
    client = client.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    client_header = client.first()
    client = client.filter(lambda line: line != client_header)

    # Create a RDD for each csv file
    clientRDD = client.map(lambda line: (line[0], line[1], line[2], line[3], line[4], line[5]))