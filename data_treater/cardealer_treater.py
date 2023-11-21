from pyspark import SparkContext

def treat_cardealer(sc: SparkContext):

    cardealer = sc.textFile("/user/hduser/cardealer.csv")
    # Split each line of the csv files by the delimiter ";"
    cardealer = cardealer.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    cardealer_header = cardealer.first()
    cardealer = cardealer.filter(lambda line: line != cardealer_header)

    # Create a RDD for each csv file
    cardealerRDD = cardealer.map(lambda line: (line[0], line[1], line[2], line[3], line[4]))