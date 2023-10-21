import streamlit as st
import pandas as pd
import datetime
from gcloud import bigquery

PROJECT_ID = "wampusfyi-402717"
TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"

client = bigquery.Client(project=PROJECT_ID)

query = "SELECT * FROM wampusfyi-402717.FormResponses.RentPrices"
client.run_sync_query(query=query)



st.title("Find Apartments")

def load_data():
    return pd.read_csv("housing_data2.csv")

data = load_data()

# Filter for School of UT
schools = st.selectbox("What school are you in?", sorted(data['School'].unique()))
data = data[data['School'] == schools]

# Filter for Bedrooms
bedrooms = st.selectbox("How many bedrooms would you prefer?", sorted(data['Bedrooms'].unique()))
data = data[data['Bedrooms'] == bedrooms]

# Filter for Bathrooms
bathrooms = st.selectbox("How many bathrooms would you prefer?", sorted(data['Bathrooms'].unique()))
data = data[data['Bathrooms'] == bathrooms]

# Filter for Price
price = st.slider("Price Range ($)", 500, 2000, (800, 1300))
data = data[(data['Rent'].astype(int) >= price[0]) & 
            (data['Rent'].astype(int) <= price[1])]


filtered_data = data[['Location', 'Bedrooms', 'Bathrooms', 'Walk Time', 'Satisfaction', 'Rent']]
st.write(filtered_data)
