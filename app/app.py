# app.py
import streamlit as st
import pandas as pd

from config import *
from utils import get_param
from visualizations import price_over_time

st.set_page_config(layout="wide")

@st.cache_data
def load_apartment_data():
    apartment_data_rows = bigquery_client.list_rows(TABLE_ID)
    apartment_data_df = apartment_data_rows.to_dataframe()
    apartment_data_df[SCHOOL] = apartment_data_df[SCHOOL].str.split(", ")
    apartment_data_df = apartment_data_df.explode(SCHOOL).reset_index(drop=True)
    apartment_data_df[LOCATION] = apartment_data_df[LOCATION].str.strip()
    apartment_data_df[SCHOOL] = apartment_data_df[SCHOOL].str.strip()
    return apartment_data_df

@st.cache_data
def load_college_data():
    college_data_rows = bigquery_client.list_rows(CLG_ADD_TABLE_ID)
    college_data_df = college_data_rows.to_dataframe()
    return college_data_df

@st.cache_data
def load_distance_data():
    distance_data_rows = bigquery_client.list_rows(DISTANCE_TABLE_ID)
    distance_data_df = distance_data_rows.to_dataframe()
    distance_data_df.columns = ['Apartment', 'School', 'Distance']
    return distance_data_df

# Load data from BigQuery
apartment_data_df = load_apartment_data()
college_data_df = load_college_data()
distance_data_df = load_distance_data()

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
        if apartment_search_input != '':  # Check if the input has text
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
        else:
            st.warning("Please enter a value to search.")

    if apartment_param:
    # Display apartment details below the search if there's a parameter in the URL or the recent search
        st.title(f"Details for {apartment_param}")
        
        specific_apartment_data = apartment_data_df[apartment_data_df[LOCATION] == apartment_param]
        specific_apartment_data_display = specific_apartment_data[[LOCATION, BEDROOMS, BATHROOMS, SATISFACTION, RENT, LEASESIGN]]

        # Ensure that LEASESIGN is in datetime format
        specific_apartment_data_display[LEASESIGN] = pd.to_datetime(specific_apartment_data_display[LEASESIGN], errors='coerce')

        # Sort the dataframe by LEASESIGN in descending order
        specific_apartment_data_display = specific_apartment_data_display.sort_values(by=LEASESIGN, ascending=False)

        specific_apartment_data_display = specific_apartment_data_display.rename(columns=rename_dict)
        
        pot_graph = price_over_time(apartment_param, bedrooms_param, bathrooms_param)

        # Create two columns for the plot and the table
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Previous Rates")
            st.write(specific_apartment_data_display.to_html(escape=False, index=False), unsafe_allow_html=True)
            
        with col2:
            if pot_graph:
                st.subheader("Monthly Rates Over Time for a {} x {} at {}".format(bedrooms_param, bathrooms_param, apartment_param))
                st.pyplot(pot_graph)

        
with findAptTab:

    st.title("Find Apartments")
    unique_colleges = college_data_df["College"].unique()

    # Filter for Bedrooms
    selected_bedrooms = st.selectbox("How many bedrooms would you prefer?", sorted(apartment_data_df[BEDROOMS].unique()))

    # Filter for Bathrooms
    selected_bathrooms = st.selectbox("How many bathrooms would you prefer?", sorted(apartment_data_df[BATHROOMS].unique()))

    # Filter for Price
    price_range = st.slider("Price Range ($)", 0, 2500, (200, 2000))
    apartments_filtered_all = apartment_data_df[
        (apartment_data_df[RENT].astype(int) >= price_range[0]) & 
        (apartment_data_df[RENT].astype(int) <= price_range[1]) &
        (apartment_data_df[BATHROOMS] == selected_bathrooms) &
        (apartment_data_df[BEDROOMS] == selected_bedrooms)
    ]
    
    if len(apartments_filtered_all) == 0:
        st.write("Unfortunately, we do not have data for the requested filters.")
    else:
        selected_college = st.selectbox("What school are you in?", unique_colleges)

        def calculate_distance(row):
            mask = (distance_data_df['Apartment'] == row[LOCATION]) & (distance_data_df['School'] == selected_college)
            matching_distance = distance_data_df[mask]['Distance'].values
            return matching_distance[0] if len(matching_distance) > 0 else None

        apartment_distance_data = apartments_filtered_all.copy()
        apartment_distance_data['Distance to {}'.format(selected_college)] = apartment_distance_data.apply(calculate_distance, axis=1)

        final_apartment_data = apartment_distance_data[[LOCATION, BEDROOMS, BATHROOMS, 'Distance to {}'.format(selected_college), SATISFACTION, RENT]]
        final_apartment_data.rename(columns=rename_dict, inplace=True)
        final_apartment_data["Apartment"] = final_apartment_data.apply(
            lambda row: f"<a target=\"_self\" href='{BASE_URL}?apartment={row['Location'].replace(' ', '%20')}&bedrooms={row['Bedrooms']}&bathrooms={row['Bathrooms']}'>{row['Location']}</a>",
            axis=1, result_type='reduce'
        )
        final_apartment_data = final_apartment_data.drop("Location", axis=1)

        final_apartment_data["Rent"] = final_apartment_data["Rent"].astype(float)  # Ensure RENT is in a numeric format
        grouped_apartment_data = final_apartment_data.groupby("Apartment", as_index=False).agg({
            "Bedrooms": "first",  # Assuming BEDROOMS, BATHROOMS, WALKTIME, SATISFACTION are the same for all rows of the same APARTMENT
            "Bathrooms": "first",
            "Satisfaction": lambda x: round(x.mean(), 2),
            "Rent": lambda x: round(x.mean(), 2),  # Calculate the average RENT
            'Distance to {}'.format(selected_college): "first"  # Assuming DISTANCE is the same for all rows of the same APARTMENT
        })
        
        grouped_apartment_data[f'Distance to {selected_college}'] = grouped_apartment_data[f'Distance to {selected_college}'].apply(lambda x: f"{x} mi." if pd.notnull(x) else "N/A")

        cols = ["Apartment"] + [col for col in grouped_apartment_data.columns if col != "Apartment"]
        grouped_apartment_data = grouped_apartment_data[cols]
        st.write("Previous Rates")
        st.write(grouped_apartment_data.to_html(escape=False, index=False), unsafe_allow_html=True)