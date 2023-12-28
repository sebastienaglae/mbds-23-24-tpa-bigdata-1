import pandas as pd
import json

end_points = ["cars", "customer_marketing", "customers", "customer_car_registration"]
ip_port = "http://135.181.84.87:8181/"

# Retrieve the data from the endpoints and store it in the df
def get_data():
    global end_points, ip_port

    car_dealer_df, marketing_df, client_df, immatriculation_df = None, None, None, None

    for end_point in end_points:
        df = pd.read_json(ip_port + end_point)
        if end_point == "cars":
            # Flatten the nested "car" structure using pd.json_normalize
            df = pd.json_normalize(df['result'], sep='_')
            car_dealer_df = df
        elif end_point == "customer_marketing":
            df = pd.json_normalize(df['result'], sep='_')
            marketing_df = df
        elif end_point == "customers":
            df = pd.json_normalize(df['result'], sep='_')
            client_df = df
        elif end_point == "customer_car_registration":
            df = pd.json_normalize(df['result'], sep='_')
            immatriculation_df = df

    return car_dealer_df, marketing_df, client_df, immatriculation_df