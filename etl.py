'''
Basic Extract, Transform and Load example
'''
#%%
import pandas as pd
import requests
from sqlalchemy import create_engine

# %%
def extract_data() -> dict:
    """ This function extracts data from the universities API."""
    API_URL = "http://universities.hipolabs.com/search?country=United+States"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error during API request:", str(e))
        return None

# %%
