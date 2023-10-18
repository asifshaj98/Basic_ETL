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
def transform(data: dict) -> pd.DataFrame:
    """ Transforms the dataset into the desired structure and filters."""
    try:
        df = pd.DataFrame(data)
        print(f"Total Number of universities from API: {len(data)}")

        # Filter universities in California
        df_california = df[df["name"].str.contains("California", case=False)]
        print(f"Number of universities in California: {len(df_california)}")

        # Join domains and web_pages lists into comma-separated strings
        df_california['domains'] = df_california['domains'].apply(lambda x: ','.join(map(str, x)))
        df_california['web_pages'] = df_california['web_pages'].apply(lambda x: ','.join(map(str, x)))

        # Reset index and select desired columns
        df_transformed = df_california.reset_index(drop=True)[["domains", "country", "web_pages", "name"]]
        return df_transformed
    except KeyError as e:
        print("Error: The input data is not in the expected format.")
        return None
    except Exception as e:
        print("An error occurred during data transformation:", str(e))
        return None


# %%
def laod(df:pd.DataFrame) -> None:
    """ Loads the data into a sqllite database"""
    db = create_engine('sqlite:///my_lite_store.db')
    df.to_sql('cal_uni', db, if_exists='replace')
# %%
