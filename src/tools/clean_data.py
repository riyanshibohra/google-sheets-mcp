# src/datacraft/tools/clean_data.py
import pandas as pd
import json

def clean_data(df_json: str, method: str = "mean") -> str:
    df = pd.read_json(df_json, orient='split')
    
    if method == "mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif method == "median":
        df = df.fillna(df.median(numeric_only=True))
    elif method == "drop":
        df = df.dropna()
    else:
        raise ValueError(f"Unknown cleaning method: {method}")
    
    return df.to_json(orient='split')
