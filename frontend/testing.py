import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "wampusfyi-402717"
TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"

client = bigquery.Client(project=PROJECT_ID)

# List rows from the table and convert to DataFrame
rows = client.list_rows(TABLE_ID)
df = rows.to_dataframe()

print(df)