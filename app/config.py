# config.py
from google.cloud import bigquery

PROJECT_ID = "wampusfyi-402717"
TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"
APT_TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"
SCHOOL = "What_school_of_UT_are_you_in"
BEDROOMS = "How_many_bedrooms_in_your_apt"
BATHROOMS = "How_many_bathrooms_in_your_apt"
RENT = "How_much_do_you_pay_monthly_just_for_the_apartment_"
WALKTIME = "What_is_your_walk_time_to_your_classes_"
SATISFACTION = "Rate_your_satisfaction_of_the_apt_from_1_10_"
LOCATION = "Where_are_you_living_this_year_"
PAGES = ["Search Apartment", "Find Apartments"]
BASE_URL = "http://localhost:8501"
CLG_ADD_TABLE_ID = "wampusfyi-402717.DistanceData.ClgAddresses"
DISTANCE_TABLE_ID = "wampusfyi-402717.DistanceData.Distances"


rename_dict = {
    LOCATION: 'LOCATION',
    BEDROOMS: 'BEDROOMS',
    BATHROOMS: 'BATHROOMS',
    WALKTIME: 'WALKTIME',
    SATISFACTION: 'SATISFACTION',
    RENT: 'RENT'
}

bigquery_client = bigquery.Client(project=PROJECT_ID)

