import pandas as pd
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import csv

PROJECT_ID = "wampusfyi-402717"
TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"

SCHOOL = "What_school_of_UT_are_you_in"
BEDROOMS = "How_many_bedrooms_in_your_apt"
BATHROOMS = "How_many_bathrooms_in_your_apt"
RENT = "How_much_do_you_pay_monthly_just_for_the_apartment_"
WALKTIME = "What_is_your_walk_time_to_your_classes_"
SATISFACTION = "Rate_your_satisfaction_of_the_apt_from_1_10_"
LOCATION = "Where_are_you_living_this_year_"
DATE = 'When_did_you_sign_your_lease___Approximations_are_cool__P_'

client = bigquery.Client(project=PROJECT_ID)

# List rows from the table and convert to DataFrame
walktime_mapping = {
    '<5 min': 1,
    '5 - 10 min': 2,
    '11 - 15 min': 3,
    '16 - 20 min': 4,
    '21+ min': 5
}

school_mapping = {
    'Cockrell': 1,
    'CNS': 2,
    'Architecture': 3,
    'Moody': 4,
    'COLA': 5,
    'McCombs': 6,
    'Fine Arts': 7,
    'Education': 8,
    'Geosciences': 9
}

apt_mapping = {
    '2400 Nueces': 	1,
'26 West'	:2,
'33rd Street Condo'	:3,
'900 W 23rd'	:4,
'Crest at Pearl':	5,
'Delphi Condominiums':	6,
'GrandMarc' 	:7,
'House in Manor'	:8,
'Inspire on 22nd':	9,
'Ion'	:10,
'Lark':	11,
'Lenox Condos':	12,
'Moontower':	13,
'Nine at Rio':	14,
'Pointe on Rio':	15,
'Quarters Nueces':	16,
'Rambler':	17,
'Rise':	18,
'Signature':	19,
'Skyloft'	:20,
'The Block on 25th'	:21,
'The Mark':	22,
'The Nine on Rio':	23,
'The Standard'	:24,
'Twenty Two 15'	:25,
'Twenty Two Fifteen'	:26,
'Villas on 26th'	:27,
'Villas on Rio':	28,
'Waterloo'	:29
}

rows = client.list_rows(TABLE_ID)
df = rows.to_dataframe()
key = df[SATISFACTION]
df = df.drop(columns=[SATISFACTION,'Timestamp',DATE])
df[SCHOOL] = df[SCHOOL].map(school_mapping)
df[WALKTIME] = df[WALKTIME].map(walktime_mapping)
df[LOCATION] = df[LOCATION].map(apt_mapping)
df[LOCATION] = df[LOCATION].astype(float)
df[WALKTIME] = df[WALKTIME].astype(float)
df[SCHOOL] = df[SCHOOL].astype(float)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)
print(df)

df_train, df_test, key_train, key_test = train_test_split(df, key, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(df_train, key_train)
y_pred = model.predict(df_test)

mse = mean_squared_error(key_test, y_pred)
r2 = r2_score(key_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")



#print(df)