from pyspark import SparkContext

def treat_inmatriculation(spark: SparkContext):
        
     #Read CSV into DataFrame
    immatriculation = spark.read.option("delimiter", ";").csv("/user/hduser/immatriculation.csv", header=True)

    # Drop rows with null values
    immatriculation = immatriculation.na.drop()
    
    # Transformer les valeurs de la colonne "couleur"
    immatriculation = immatriculation.map(lambda cols: (
        cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], "grise" if cols[7] == "gris" else "blanche" if cols[7] == "blanc" else "bleue" if cols[7] == "bleu" else cols[7], cols[8], cols[9]
    ))
    
    #Supprimer les lignes avec des caracteres "?"
    immatriculation = immatriculation.filter(lambda row: all("?" not in col for col in row))
    
    # Afficher le résultat
    for row in immatriculation.collect():
        print(row)