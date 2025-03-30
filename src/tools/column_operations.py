import pandas as pd
from typing import Dict, List, Any, Union
import numpy as np

def add_column(df_json: str, new_column_name: str, formula: str, reference_columns: List[str]) -> str:
    """
    Add a new column based on calculations from other columns
    Args:
        df_json: DataFrame in JSON format
        new_column_name: Name of the new column
        formula: Type of operation to perform ('concat', 'sum', 'multiply', 'divide', 'subtract')
        reference_columns: List of columns to use in the calculation
    """
    df = pd.read_json(df_json, orient='split')
    
    # Validate reference columns exist
    if not all(col in df.columns for col in reference_columns):
        invalid_cols = [col for col in reference_columns if col not in df.columns]
        raise ValueError(f"Invalid reference columns: {invalid_cols}")
    
    # Check if new column name already exists
    if new_column_name in df.columns:
        raise ValueError(f"Column '{new_column_name}' already exists")
    
    # Apply the formula
    if formula == 'concat':
        df[new_column_name] = df[reference_columns].astype(str).agg(' '.join, axis=1)
    elif formula == 'sum':
        df[new_column_name] = df[reference_columns].sum(axis=1)
    elif formula == 'multiply':
        df[new_column_name] = df[reference_columns].prod(axis=1)
    elif formula == 'divide':
        if len(reference_columns) != 2:
            raise ValueError("Division requires exactly 2 reference columns")
        df[new_column_name] = df[reference_columns[0]] / df[reference_columns[1]]
    elif formula == 'subtract':
        if len(reference_columns) != 2:
            raise ValueError("Subtraction requires exactly 2 reference columns")
        df[new_column_name] = df[reference_columns[0]] - df[reference_columns[1]]
    else:
        raise ValueError(f"Unsupported formula: {formula}")
    
    return df.to_json(orient='split')

def rename_column(df_json: str, old_name: str, new_name: str) -> str:
    """Rename a column"""
    df = pd.read_json(df_json, orient='split')
    
    if old_name not in df.columns:
        raise ValueError(f"Column '{old_name}' not found")
    if new_name in df.columns:
        raise ValueError(f"Column '{new_name}' already exists")
    
    df = df.rename(columns={old_name: new_name})
    return df.to_json(orient='split')

def transform_column(df_json: str, column_name: str, transformation: str, params: Dict = None) -> str:
    """
    Transform values in a column
    Args:
        df_json: DataFrame in JSON format
        column_name: Name of the column to transform
        transformation: Type of transformation ('uppercase', 'lowercase', 'round', 'format_date')
        params: Additional parameters for the transformation
    """
    df = pd.read_json(df_json, orient='split')
    params = params or {}
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found")
    
    if transformation == 'uppercase':
        df[column_name] = df[column_name].astype(str).str.upper()
    elif transformation == 'lowercase':
        df[column_name] = df[column_name].astype(str).str.lower()
    elif transformation == 'round':
        decimals = params.get('decimals', 0)
        df[column_name] = df[column_name].round(decimals)
    elif transformation == 'format_date':
        date_format = params.get('format', '%Y-%m-%d')
        df[column_name] = pd.to_datetime(df[column_name]).dt.strftime(date_format)
    else:
        raise ValueError(f"Unsupported transformation: {transformation}")
    
    return df.to_json(orient='split') 