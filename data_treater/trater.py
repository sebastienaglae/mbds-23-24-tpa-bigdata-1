from pyspark import SparkContext


def treat_cardealer(sc):

    cardealer = sc.textFile("/user/hduser/cardealer.csv")
    # Split each line of the csv files by the delimiter ";"
    cardealer = cardealer.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    cardealer_header = cardealer.first()
    cardealer = cardealer.filter(lambda line: line != cardealer_header)

    # Create a RDD for each csv file
    cardealerRDD = cardealer.map(lambda line: (line[0], line[1], line[2], line[3], line[4]))

def treat_client(sc):
    
    client = sc.textFile("/user/hduser/client.csv")
    # Split each line of the csv files by the delimiter ";"
    client = client.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    client_header = client.first()
    client = client.filter(lambda line: line != client_header)

    # Create a RDD for each csv file
    clientRDD = client.map(lambda line: (line[0], line[1], line[2], line[3], line[4], line[5]))

def treat_inmatriculation(sc):
        
    inmatriculation = sc.textFile("/user/hduser/inmatriculation.csv")
    # Split each line of the csv files by the delimiter ";"
    inmatriculation = inmatriculation.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    inmatriculation_header = inmatriculation.first()
    inmatriculation = inmatriculation.filter(lambda line: line != inmatriculation_header)

    # Create a RDD for each csv file
    inmatriculationRDD = inmatriculation.map(lambda line: (line[0], line[1], line[2], line[3]))

def treat_marketing(sc):
            
    marketing = sc.textFile("/user/hduser/marketing.csv")
    # Split each line of the csv files by the delimiter ";"
    marketing = marketing.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    marketing_header = marketing.first()
    marketing = marketing.filter(lambda line: line != marketing_header)

    # Create a RDD for each csv file
    marketingRDD = marketing.map(lambda line: (line[0], line[1], line[2], line[3], line[4]))

def treat_all():
    # Create a SparkContext object
    sc = SparkContext(appName="TreaterApplication")

    treat_cardealer(sc)
    treat_client(sc)
    treat_inmatriculation(sc)
    treat_marketing(sc)
    
    # Stop the SparkContext when you're done
    sc.stop()

if __name__ == "__main__":
    treat_all()



