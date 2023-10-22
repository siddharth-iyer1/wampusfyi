# app.py
import streamlit as st
import pandas as pd

from config import *
from utils import get_param
from visualizations import price_over_time
import pydeck as pdk
from googlemaps import Client
import json

api_key = "AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc"
gm_client = Client(api_key)

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

st.markdown(f"<h1><span style='color: #cc5500'>Wampus.FYI</span>: UT Austin West Campus Apartment Info</h1>", unsafe_allow_html=True)

apt_rows = bigquery_client.list_rows(APT_TABLE_ID)
apt_df = apt_rows.to_dataframe()
geocode_result = []
for i in apt_df["Address"]:
    geocode_result.append(gm_client.geocode(i))
apt_df['coords'] = geocode_result
marker_data = []
lats = []
lons = []

for i in range(len(apt_df)):
    lats.append(apt_df['coords'][i][0]['geometry']['location']['lat'])
    lons.append(apt_df['coords'][i][0]['geometry']['location']['lng'])

for i,row in apt_df.iterrows():
    marker_data.append({"name": row['Apartment'], "lat": lats[i], "lon": lons[i]})
    
marker_layer = pdk.Layer(
    "ScatterplotLayer",
    data=marker_data,
    get_position=["lon", "lat"],
    get_radius=25,  # Adjust the marker size as needed
    get_fill_color=[191, 87, 0],  # RGB color for markers (green in this example)
)

view_state = pdk.ViewState(
    latitude=30.2883838,  # Center latitude
    longitude=-97.7434334,  # Center longitude
    zoom=14,  # Adjust the zoom level as needed
)

r = pdk.Deck(
    layers=[marker_layer],
    initial_view_state=view_state,
)
st.pydeck_chart(r)

st.subheader("Apartment Finder")

# Create tabs
searchAptTab, findAptTab = st.tabs(["Search Apartment", "Find Apartment"])

with searchAptTab:
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    apartment_search_input = st.text_input("Search for an apartment:", value=apartment_param if apartment_param else '')
    search_button_clicked = st.button("Search")

    if search_button_clicked:
        if apartment_search_input != "":
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
            st.warning("Please enter a value to search")

    if apartment_param:
    # Display apartment details below the search if there's a parameter in the URL or the recent search
        st.markdown(f"<h1>Details for <spa style='color: #cc5500'>{apartment_param}</span></h1>", unsafe_allow_html=True)

        
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
    col1, gap1, col2 = st.columns([8,1,8])

    # Reserve space for widgets
    with col1:
        bedroom_space = st.empty()
        ""
        bathroom_space = st.empty()

    with col2:
        price_space = st.empty()
        college_space = st.empty()

    # Add widgets to the reserved spaces
    selected_bedrooms = bedroom_space.selectbox("How many bedrooms would you prefer?", sorted(apartment_data_df[BEDROOMS].unique()), 3)
    selected_bathrooms = bathroom_space.selectbox("How many bathrooms would you prefer?", sorted(apartment_data_df[BATHROOMS].unique()), 3)
    price_range = price_space.slider("Price Range ($)", 100, 2000, (200, 1900))
    selected_college = college_space.selectbox("What school are you in?", unique_colleges)

    apartments_filtered_all = apartment_data_df[
        (apartment_data_df[RENT].astype(int) >= price_range[0]) & 
        (apartment_data_df[RENT].astype(int) <= price_range[1]) &
        (apartment_data_df[BATHROOMS] == selected_bathrooms) &
        (apartment_data_df[BEDROOMS] == selected_bedrooms)
    ]
    
    if len(apartments_filtered_all) == 0:
        st.write("Unfortunately, we do not have data for the requested filters.")
    else:
        def calculate_distance(row):
            mask = (distance_data_df['Apartment'] == row[LOCATION]) & (distance_data_df['School'] == selected_college)
            matching_distance = distance_data_df[mask]['Distance'].values
            return matching_distance[0] if len(matching_distance) > 0 else None

        apartment_distance_data = apartments_filtered_all.copy()
        apartment_distance_data['Distance to {}'.format(selected_college)] = apartment_distance_data.apply(calculate_distance, axis=1)

        final_apartment_data = apartment_distance_data[[LOCATION, BEDROOMS, BATHROOMS, 'Distance to {}'.format(selected_college), SATISFACTION, RENT]]
        final_apartment_data.rename(columns=rename_dict, inplace=True)
        final_apartment_data["Apartment"] = final_apartment_data.apply(
            lambda row: f"<a style='color: #cc5500;' target=\"_self\" href='{BASE_URL}?apartment={row['Location'].replace(' ', '%20')}&bedrooms={row['Bedrooms']}&bathrooms={row['Bathrooms']}#apartment-finder'>{row['Location']}</a>",
            axis=1, result_type='reduce'
        )
        # final_apartment_data = final_apartment_data.drop("Location", axis=1)

        final_apartment_data["Rent"] = final_apartment_data["Rent"].astype(float)  # Ensure RENT is in a numeric format
        grouped_apartment_data = final_apartment_data.groupby("Apartment", as_index=False).agg({
            "Bedrooms": "first",  # Assuming BEDROOMS, BATHROOMS, WALKTIME, SATISFACTION are the same for all rows of the same APARTMENT
            "Bathrooms": "first",
            "Satisfaction": lambda x: round(x.mean(), 2),
            "Rent": lambda x: round(x.mean(), 2),  # Calculate the average RENT
            'Distance to {}'.format(selected_college): "first",  # Assuming DISTANCE is the same for all rows of the same APARTMENT
            "Location": "first"
        })
        
        grouped_apartment_data[f'Distance to {selected_college}'] = grouped_apartment_data[f'Distance to {selected_college}'].apply(lambda x: f"{x} mi." if pd.notnull(x) else "N/A")

        cols = ["Apartment"] + [col for col in grouped_apartment_data.columns if col != "Apartment"]
        grouped_apartment_data = grouped_apartment_data[cols]
        
        ""
        ""
        
        if len(grouped_apartment_data) > 0:
            # Extract summary information
            highest_satisfaction = grouped_apartment_data.loc[grouped_apartment_data["Satisfaction"].idxmax()]
            lowest_rent = grouped_apartment_data.loc[grouped_apartment_data["Rent"].idxmin()]
            closest_distance = grouped_apartment_data.loc[grouped_apartment_data['Distance to {}'.format(selected_college)].idxmin()]
            # Create columns for layout
            col1, col2 = st.columns([2, 1])

            with col1:
                
                tabledat = grouped_apartment_data
                tabledat = tabledat.drop("Location", axis=1)
                tabledat = tabledat.sort_values(by='Rent')
                st.subheader("Previous Rates")
                st.write(tabledat.to_html(escape=False, index=False), unsafe_allow_html=True)
                
            with col2:
                st.subheader("Summary")
                summary_items = [
                    {"label": "Highest Average Satisfaction", "value": f"{highest_satisfaction['Location']} ({highest_satisfaction['Satisfaction']} satisfaction)"},
                    {"label": "Lowest Average Rent", "value": f"{lowest_rent['Location']} (${lowest_rent['Rent']} per month)"},
                    {"label": f"Closest Distance to {selected_college}", "value": f"{closest_distance['Location']} ({closest_distance['Distance to {}'.format(selected_college)]} mi)"}
                ]
                
                for item in summary_items:
                    with st.container():
                        st.markdown(f"###### {item['label']}")
                        st.markdown(f"<div style='font-size: 1em;'>{item['value']}</div>", unsafe_allow_html=True)
                        st.markdown("---")  # Optional: Add a divider line