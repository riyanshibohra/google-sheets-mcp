from tools.fetch_sheet import fetch_sheet
import json
import pandas as pd

def test_fetch_sheet():
    # Example Google Sheet URL - replace with your test sheet URL
    test_sheet_url = "https://docs.google.com/spreadsheets/d/1FK5Dpq1sXIYlj_uZiBSvJrKW6XpV9I_Pue-jdELi9qw/edit?usp=sharing"
    test_tab_name = "Sheet1" 

    try:
        # Fetch the data
        result_json = fetch_sheet(test_sheet_url, test_tab_name)
        
        # Convert JSON string back to DataFrame
        df = pd.read_json(result_json, orient='split')
        
        # Print basic information about the fetched data
        print("\nFetch successful! Here's what we got:")
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst few rows:")
        print(df.head())
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_fetch_sheet() 