import pandas as pd
from gcloud import bigquery


PROJECT_ID = "wampusfyi-402717"
TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"

client = bigquery.Client(project=PROJECT_ID)

dataset_ref = client.dataset('FormResponses')
table_ref = dataset_ref.table('RentPrices')
table = client.get_table(table_ref)  # This is where you use the get_table method

print(table)