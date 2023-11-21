from pyspark import SparkContext
from cardealer_treater import treat_cardealer
from client_treater import treat_client
from inmatriculation_treater import treat_inmatriculation
from marketing_treater import treat_marketing

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



