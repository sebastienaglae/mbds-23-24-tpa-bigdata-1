from pyspark import SparkContext

def treat_inmatriculation(sc: SparkContext):
        
    inmatriculation = sc.textFile("/user/hduser/inmatriculation.csv")
    # Split each line of the csv files by the delimiter ";"
    inmatriculation = inmatriculation.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    inmatriculation_header = inmatriculation.first()
    inmatriculation = inmatriculation.filter(lambda line: line != inmatriculation_header)

    # Create a RDD for each csv file
    inmatriculationRDD = inmatriculation.map(lambda line: (line[0], line[1], line[2], line[3]))