import pandas as pd
import requests

end_points = ["cars", "customer_marketing", "customers", "customer_car_registration"]
ip_port = "http://135.181.84.87:8181/"

# Function to retrieve data from a paginated endpoint
def get_paginated_data(endpoint, page_size=1000000):
    page = 1
    all_data = []

    while True:
        url = f"{ip_port}{endpoint}?page={page}&size={page_size}"
        response = requests.get(url)

        if not response.ok:
            break

        data = response.json().get("result", [])
        df = pd.json_normalize(data, sep="_")
        all_data.append(df)

        # Check if there are more pages
        if len(data) < page_size:
            break

        page += 1

    return pd.concat(all_data, ignore_index=True)

# Retrieve the data from the endpoints and store it in the DataFrame
def get_data(endpoints : list = end_points):

    car_dealer_df, marketing_df, client_df, immatriculation_df = None, None, None, None

    for end_point in endpoints:
        df = get_paginated_data(end_point)
        
        if end_point == "cars":
            car_dealer_df = df
        elif end_point == "customer_marketing":
            marketing_df = df
        elif end_point == "customers":
            client_df = df
        elif end_point == "customer_car_registration":
            immatriculation_df = df

    return car_dealer_df, marketing_df, client_df, immatriculation_df