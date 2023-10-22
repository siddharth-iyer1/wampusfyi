# app.py
import streamlit as st
from google.cloud import bigquery
import pandas as pd

from config import *
from utils import get_param
from visualizations import price_over_time

rows = bigquery_client.list_rows(TABLE_ID)
data = rows.to_dataframe()

data[SCHOOL] = data[SCHOOL].str.split(", ")
data = data.explode(SCHOOL).reset_index(drop=True)

apartment_param = get_param("apartment")
bedrooms_param = get_param("bedrooms")
bathrooms_param = get_param("bathrooms")

searchApt, findApt = st.tabs(PAGES)

with searchApt:
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    searched_apartment = st.text_input("Search for an apartment:", value=apartment_param if apartment_param else '')
    search_button = st.button("Search")

    if search_button:
        if searched_apartment in data[LOCATION].unique():
            apartment_param = searched_apartment  # set apartment_param to the newly searched apartment
            st.experimental_set_query_params(apartment=searched_apartment)  # this line can be removed if not necessary
        else:
            st.write("Apt not found")

    if apartment_param:
        # Display apartment details below the search if there's a parameter in the URL or the recent search
        st.title(f"Details for {apartment_param}")
        st.write("Here you can add more details or data visualizations for the apartment.")
        st.pyplot(price_over_time(apartment_param, bedrooms_param, bathrooms_param))

        
with findApt:

    st.title("Find Apartments")

    # Filter for School of UT
    schools = st.selectbox("What school are you in?", sorted(data[SCHOOL].unique()))
    data = data[data[SCHOOL] == schools]

    # Filter for Bedrooms
    bedrooms = st.selectbox("How many bedrooms would you prefer?", sorted(data[BEDROOMS].unique()))
    data = data[data[BEDROOMS] == bedrooms]

    # Filter for Bathrooms
    bathrooms = st.selectbox("How many bathrooms would you prefer?", sorted(data[BATHROOMS].unique()))
    data = data[data[BATHROOMS] == bathrooms]

    # Filter for Price
    price = st.slider("Price Range ($)", 500, 2000, (800, 1300))
    data = data[(data[RENT].astype(int) >= price[0]) & 
                (data[RENT].astype(int) <= price[1])]


    distance_data = pd.read_csv('datasets/distance_data.csv', header=None, names=['Apartment', 'School', 'Distance'])

    def get_distance(row):
        mask = (distance_data['Apartment'] == row[LOCATION]) & (distance_data['School'] == row[SCHOOL])
        matching_distance = distance_data[mask]['Distance'].values
        return matching_distance[0] if len(matching_distance) > 0 else None

    # Apply the get_distance function row-wise to get the 'WalkTimeMajor' column

    filtered_data = data[[LOCATION, BEDROOMS, BATHROOMS, WALKTIME, SATISFACTION, RENT, SCHOOL]]
    filtered_data['DISTANCE'] = filtered_data.apply(get_distance, axis=1)
    filtered_data = filtered_data[[LOCATION, BEDROOMS, BATHROOMS, "DISTANCE", SATISFACTION, RENT]]
    filtered_data.rename(columns=rename_dict, inplace=True)

    base_url = "http://localhost:8501?apartment="
    
    filtered_data["APARTMENT"] = filtered_data.apply(
        lambda row: f"<a target=\"_self\" href='http://localhost:8501?apartment={row['LOCATION'].replace(' ', '%20')}&bedrooms={row['BEDROOMS']}&bathrooms={row['BATHROOMS']}'>{row['LOCATION']}</a>",
        axis=1, result_type='reduce'
    )
    filtered_data = filtered_data.drop("LOCATION", axis=1)

    cols = ["APARTMENT"] + [col for col in filtered_data if col != "APARTMENT"]
    filtered_data = filtered_data[cols]
    st.write("Previous Rates")
    st.write(filtered_data.to_html(escape=False, index=False), unsafe_allow_html=True)