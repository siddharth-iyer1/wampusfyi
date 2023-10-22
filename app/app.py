# app.py
import streamlit as st
import pandas as pd

from config import *
from utils import get_param
from visualizations import price_over_time

# Load data from BigQuery
apartment_data_rows = bigquery_client.list_rows(TABLE_ID)
apartment_data_df = apartment_data_rows.to_dataframe()
apartment_data_df[SCHOOL] = apartment_data_df[SCHOOL].str.split(", ")
apartment_data_df = apartment_data_df.explode(SCHOOL).reset_index(drop=True)
apartment_data_df[LOCATION] = apartment_data_df[LOCATION].str.strip()
apartment_data_df[SCHOOL] = apartment_data_df[SCHOOL].str.strip()

# Load college data from BigQuery
college_data_rows = bigquery_client.list_rows(CLG_ADD_TABLE_ID)
college_data_df = college_data_rows.to_dataframe()

# Load distance data from BigQuery
distance_data_rows = bigquery_client.list_rows(DISTANCE_TABLE_ID)
distance_data_df = distance_data_rows.to_dataframe()
distance_data_df.columns = ['Apartment', 'School', 'Distance']

print(distance_data_df["Apartment"].unique())

# Get parameters from URL
apartment_param = get_param("apartment")
bedrooms_param = get_param("bedrooms")
bathrooms_param = get_param("bathrooms")

# Create tabs
searchAptTab, findAptTab = st.tabs(PAGES)

with searchAptTab:
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    apartment_search_input = st.text_input("Search for an apartment:", value=apartment_param if apartment_param else '')
    search_button_clicked = st.button("Search")

    if search_button_clicked:
        cleaned_input = apartment_search_input.strip().lower()
        cleaned_apartment_names = apartment_data_df[LOCATION].str.strip().str.lower().unique()
        if cleaned_input in cleaned_apartment_names:
            # Convert back to original case to use as parameter
            original_case_apartment = apartment_data_df[apartment_data_df[LOCATION].str.strip().str.lower() == cleaned_input][LOCATION].values[0]
            apartment_param = original_case_apartment
            st.experimental_set_query_params(apartment=original_case_apartment)
            st.experimental_rerun()
        else:
            st.write("Apartment not found")

    if apartment_param:
        # Display apartment details below the search if there's a parameter in the URL or the recent search
        st.title(f"Details for {apartment_param}")
        
        specific_apartment_data = apartment_data_df[apartment_data_df[LOCATION] == apartment_param]
        specific_apartment_data_display = specific_apartment_data[[LOCATION, BEDROOMS, BATHROOMS, SATISFACTION, RENT, LEASESIGN]]
        specific_apartment_data_display = specific_apartment_data_display.rename(columns=rename_dict)
        st.subheader("Previous Rates")
        
        st.write(specific_apartment_data_display.to_html(escape=False, index=False), unsafe_allow_html=True)
        ""
        ""
        ""
        pot_graph = price_over_time(apartment_param, bedrooms_param, bathrooms_param)
        if pot_graph:
            st.pyplot(pot_graph)

        
with findAptTab:

    st.title("Find Apartments")
    unique_colleges = college_data_df["College"].unique()

    # Filter for Bedrooms
    selected_bedrooms = st.selectbox("How many bedrooms would you prefer?", sorted(apartment_data_df[BEDROOMS].unique()))
    apartments_filtered_bedrooms = apartment_data_df[apartment_data_df[BEDROOMS] == selected_bedrooms]

    # Filter for Bathrooms
    selected_bathrooms = st.selectbox("How many bathrooms would you prefer?", sorted(apartments_filtered_bedrooms[BATHROOMS].unique()))
    apartments_filtered_bedrooms_bathrooms = apartments_filtered_bedrooms[apartments_filtered_bedrooms[BATHROOMS] == selected_bathrooms]

    # Filter for Price
    price_range = st.slider("Price Range ($)", 0, 2500, (200, 2000))
    apartments_filtered_all = apartments_filtered_bedrooms_bathrooms[(apartments_filtered_bedrooms_bathrooms[RENT].astype(int) >= price_range[0]) & (apartments_filtered_bedrooms_bathrooms[RENT].astype(int) <= price_range[1])]
    
    if len(apartments_filtered_all) == 0:
        st.write("Unfortunately, we do not have data for the requested filters.")
    else:
        selected_college = st.selectbox("What school are you in?", unique_colleges)

        def calculate_distance(row):
            mask = (distance_data_df['Apartment'] == row[LOCATION]) & (distance_data_df['School'] == selected_college)
            matching_distance = distance_data_df[mask]['Distance'].values
            return matching_distance[0] if len(matching_distance) > 0 else None

        apartment_distance_data = apartments_filtered_all.copy()
        apartment_distance_data['DISTANCE'] = apartment_distance_data.apply(calculate_distance, axis=1)

        final_apartment_data = apartment_distance_data[[LOCATION, BEDROOMS, BATHROOMS, "DISTANCE", SATISFACTION, RENT]]
        final_apartment_data.rename(columns=rename_dict, inplace=True)
        final_apartment_data["APARTMENT"] = final_apartment_data.apply(
            lambda row: f"<a target=\"_self\" href='{BASE_URL}?apartment={row['LOCATION'].replace(' ', '%20')}&bedrooms={row['BEDROOMS']}&bathrooms={row['BATHROOMS']}'>{row['LOCATION']}</a>",
            axis=1, result_type='reduce'
        )
        final_apartment_data = final_apartment_data.drop("LOCATION", axis=1)

        final_apartment_data["RENT"] = final_apartment_data["RENT"].astype(float)  # Ensure RENT is in a numeric format
        grouped_apartment_data = final_apartment_data.groupby("APARTMENT", as_index=False).agg({
            "BEDROOMS": "first",  # Assuming BEDROOMS, BATHROOMS, WALKTIME, SATISFACTION are the same for all rows of the same APARTMENT
            "BATHROOMS": "first",
            "SATISFACTION": lambda x: round(x.mean(), 2),
            "RENT": lambda x: round(x.mean(), 2),  # Calculate the average RENT
            "DISTANCE": "first"  # Assuming DISTANCE is the same for all rows of the same APARTMENT
        })

        cols = ["APARTMENT"] + [col for col in grouped_apartment_data.columns if col != "APARTMENT"]
        grouped_apartment_data = grouped_apartment_data[cols]
        st.write("Previous Rates")
        st.write(grouped_apartment_data.to_html(escape=False, index=False), unsafe_allow_html=True)