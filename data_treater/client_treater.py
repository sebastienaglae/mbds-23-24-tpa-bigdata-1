from pyspark import SparkContext

def treat_client(spark: SparkContext):


     #Read CSV into DataFrame
    client = spark.read.option("delimiter", ";").csv("/user/hduser/client.csv", header=True)

    # Drop rows with null values
    client = client.na.drop()
    
     # Transformer les valeurs de la colonne "sexe"
    client = client.map(lambda cols: (cols[0], "Homme" if cols[1] in ["Homme", "H", "Masculin"] else "Femme" if cols[1] in ["Femme", "Féminin"] else cols[1], cols[2], cols[3], cols[4], cols[5], cols[6]))
    
     #Effacer les lignes avec des elements NaN dans toutes les colonnes du fichier client
    client = client.filter(lambda row: all(col is not None for col in row))
    
    #Effacer les lignes ayant des carateres "?" dans toutes les colonnes du fichier client
    client = client.filter(lambda row: all("?" not in col for col in row))
    
    #Remplacons les elements "Seul" et "Seule" par "Celibataire" et "Marie(e)" par "En couple". On conserve uniquement "En couple" et "Célibataire"
    client = client.map(lambda cols: (cols[0], cols[1], cols[2], "Célibataire" if cols[3] in ["Célibataire"] else "En couple" if cols[3] in ["En couple", "Marié(e)"] else "Célibataire", cols[2], cols[3], cols[4], cols[5], cols[6]))


    # Afficher le client résultant
    for row in client.collect():
        print(row)
        
   
