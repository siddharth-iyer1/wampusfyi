# utils.py
import pandas as pd
from google.cloud import bigquery
import streamlit as st

from config import PROJECT_ID, TABLE_ID

def load_data():
    client = bigquery.Client(project=PROJECT_ID)
    rows = client.list_rows(TABLE_ID)
    data = rows.to_dataframe()
    return data

def get_param(param):
    params = st.experimental_get_query_params()
    param_value = params.get(param)
    if param_value:
        return param_value[0]
    return None
