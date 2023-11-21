from pyspark import SparkContext

def treat_client(sc: SparkContext):
    
    client = sc.textFile("/user/hduser/client.csv")
    # Split each line of the client.csv file by the delimiter ";"
    client = client.map(lambda line: line.split(";"))

    # Remove the header for the client.csv file
    client_header = client.first()
    client = client.filter(lambda line: line != client_header)

    # Create a RDD for the client.csv file
    clientRDD = client.map(lambda line: (line[0], line[1], line[2], line[3], line[4], line[5]))
    
     # Transformer les valeurs de la colonne "sexe"
    clientRDD = clientRDD.map(lambda cols: (cols[0], "Homme" if cols[1] in ["Homme", "H", "Masculin"] else "Femme" if cols[1] in ["Femme", "Féminin"] else cols[1], cols[2], cols[3], cols[4], cols[5]))
    
     #Effacer les lignes avec des elements NaN dans toutes les colonnes du fichier client
    clientRDD = clientRDD.filter(lambda row: all(col is not None for col in row))
    
    #Effacer les lignes ayant des carateres "?" dans toutes les colonnes du fichier client
    clientRDD = clientRDD.filter(lambda row: all("?" not in col for col in row))
    
    #Remplacons les elements "Seul" et "Seule" par "Celibataire" et "Marie(e)" par "En couple". On conserve uniquement "En couple" et "Célibataire"
    clientRDD = clientRDD.map(lambda cols: (cols[0], "Célibataire" if cols[1] in ["Célibataire"] else "En couple" if cols[1] in ["En couple", "Marié(e)"] else "Célibataire", cols[2], cols[3], cols[4], cols[5]))


    # Afficher le RDD résultant
    for row in clientRDD.collect():
        print(row)
        
   
