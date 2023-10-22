# utils.py
import pandas as pd
from google.cloud import bigquery
import streamlit as st

def get_param(param):
    params = st.experimental_get_query_params()
    param_value = params.get(param)
    if param_value:
        return param_value[0]
    return None
