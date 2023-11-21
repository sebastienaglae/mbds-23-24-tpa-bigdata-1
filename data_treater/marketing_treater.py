from pyspark import SparkContext

def treat_marketing(sc: SparkContext):
            
    marketing = sc.textFile("/user/hduser/marketing.csv")
    # Split each line of the csv files by the delimiter ";"
    marketing = marketing.map(lambda line: line.split(";"))

    # Remove the header of each csv file
    marketing_header = marketing.first()
    marketing = marketing.filter(lambda line: line != marketing_header)

    # Create a RDD for each csv file
    marketingRDD = marketing.map(lambda line: (line[0], line[1], line[2], line[3], line[4]))