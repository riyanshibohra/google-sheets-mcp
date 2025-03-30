import pandas as pd
from typing import Dict, List, Any, Union
import numpy as np

def add_column(df: pd.DataFrame, new_column_name: str, formula: str, reference_columns: List[str], params: Dict = None) -> pd.DataFrame:
    """
    Add a new column based on calculations from other columns
    Args:
        df: Input DataFrame
        new_column_name: Name of the new column
        formula: Type of operation to perform ('concat', 'sum', 'multiply', 'divide', 'subtract')
        reference_columns: List of columns to use in the calculation
        params: Additional parameters for string operations
            - separator: str, separator for concat operation (default: ' ')
            - prefix: str, text to add before the concatenation
            - suffix: str, text to add after the concatenation
            - format_string: str, Python format string for advanced formatting
    """
    df_copy = df.copy()
    params = params or {}
    
    # Validate reference columns exist
    if not all(col in df_copy.columns for col in reference_columns):
        invalid_cols = [col for col in reference_columns if col not in df_copy.columns]
        raise ValueError(f"Invalid reference columns: {invalid_cols}")
    
    # Check if new column name already exists
    if new_column_name in df_copy.columns:
        raise ValueError(f"Column '{new_column_name}' already exists")
    
    # Apply the formula
    if formula == 'concat':
        separator = str(params.get('separator', ' '))  # Ensure separator is a string
        prefix = str(params.get('prefix', ''))
        suffix = str(params.get('suffix', ''))
        format_string = params.get('format_string', None)
        
        if format_string:
            # Use Python string formatting if format_string is provided
            df_copy[new_column_name] = df_copy[reference_columns].apply(
                lambda row: format_string.format(*[str(val) for val in row]), axis=1
            )
        else:
            # Convert all values to string and join with separator
            values = df_copy[reference_columns].astype(str).apply(
                lambda row: separator.join(row.values.astype(str)), axis=1
            )
            df_copy[new_column_name] = prefix + values + suffix
            
    elif formula == 'sum':
        df_copy[new_column_name] = df_copy[reference_columns].sum(axis=1)
    elif formula == 'multiply':
        df_copy[new_column_name] = df_copy[reference_columns].prod(axis=1)
    elif formula == 'divide':
        if len(reference_columns) != 2:
            raise ValueError("Division requires exactly 2 reference columns")
        df_copy[new_column_name] = df_copy[reference_columns[0]] / df_copy[reference_columns[1]]
    elif formula == 'subtract':
        if len(reference_columns) != 2:
            raise ValueError("Subtraction requires exactly 2 reference columns")
        df_copy[new_column_name] = df_copy[reference_columns[0]] - df_copy[reference_columns[1]]
    else:
        raise ValueError(f"Unsupported formula: {formula}")
    
    return df_copy

def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """Rename a column"""
    df_copy = df.copy()
    
    if old_name not in df_copy.columns:
        raise ValueError(f"Column '{old_name}' not found")
    if new_name in df_copy.columns:
        raise ValueError(f"Column '{new_name}' already exists")
    
    return df_copy.rename(columns={old_name: new_name})

def transform_column(df: pd.DataFrame, column_name: str, transformation: str, params: Dict = None) -> pd.DataFrame:
    """
    Transform values in a column
    Args:
        df: Input DataFrame
        column_name: Name of the column to transform
        transformation: Type of transformation ('uppercase', 'lowercase', 'round', 'format_date')
        params: Additional parameters for the transformation
    """
    df_copy = df.copy()
    params = params or {}
    
    if column_name not in df_copy.columns:
        raise ValueError(f"Column '{column_name}' not found")
    
    if transformation == 'uppercase':
        df_copy[column_name] = df_copy[column_name].astype(str).str.upper()
    elif transformation == 'lowercase':
        df_copy[column_name] = df_copy[column_name].astype(str).str.lower()
    elif transformation == 'round':
        decimals = params.get('decimals', 0)
        df_copy[column_name] = df_copy[column_name].round(decimals)
    elif transformation == 'format_date':
        date_format = params.get('format', '%Y-%m-%d')
        df_copy[column_name] = pd.to_datetime(df_copy[column_name]).dt.strftime(date_format)
    else:
        raise ValueError(f"Unsupported transformation: {transformation}")
    
    return df_copy 