import pandas as pd


end_points = ["car_dealer", "marketing", "client", "immatriculation"]
ip_port = "http://135.181.84.87:8181/"

# Retrieve the data from the endpoints and store it in the df
def get_data():

    for end_point in end_points:
        df = pd.read_json(ip_port + end_point)
        if end_point == "car_dealer":
            car_dealer_df = df
        elif end_point == "marketing":
            marketing_df = df
        elif end_point == "client":
            client_df = df
        elif end_point == "immatriculation":
            immatriculation_df = df

    return car_dealer_df, marketing_df, client_df, immatriculation_df