import pandas as pd
from typing import Dict, Any

def add_data(df: pd.DataFrame, row_data: Dict[str, Any]) -> pd.DataFrame:
    """Add a new row to the dataset"""
    # Validate that all columns exist
    if not all(col in df.columns for col in row_data.keys()):
        invalid_cols = [col for col in row_data.keys() if col not in df.columns]
        raise ValueError(f"Invalid columns: {invalid_cols}")
    
    # Add new row using concat
    new_df = pd.DataFrame([row_data])
    return pd.concat([df, new_df], ignore_index=True)

def edit_data(df: pd.DataFrame, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> pd.DataFrame:
    """Edit an existing row"""
    # Validate columns
    if not all(col in df.columns for col in row_identifier.keys()):
        invalid_cols = [col for col in row_identifier.keys() if col not in df.columns]
        raise ValueError(f"Invalid identifier columns: {invalid_cols}")
    
    if not all(col in df.columns for col in updated_data.keys()):
        invalid_cols = [col for col in updated_data.keys() if col not in df.columns]
        raise ValueError(f"Invalid update columns: {invalid_cols}")
    
    # Create mask for identifying the row
    mask = pd.Series(True, index=df.index)
    for col, value in row_identifier.items():
        mask &= (df[col] == value)
    
    # Check if row exists
    if not mask.any():
        raise ValueError(f"No row found matching identifier: {row_identifier}")
    
    # Update data
    df_copy = df.copy()
    for field, value in updated_data.items():
        df_copy.loc[mask, field] = value
    
    return df_copy

def delete_data(df: pd.DataFrame, row_identifier: Dict[str, Any]) -> pd.DataFrame:
    """Delete a row"""
    # Validate columns
    if not all(col in df.columns for col in row_identifier.keys()):
        invalid_cols = [col for col in row_identifier.keys() if col not in df.columns]
        raise ValueError(f"Invalid identifier columns: {invalid_cols}")
    
    # Create mask for identifying the row
    mask = pd.Series(True, index=df.index)
    for col, value in row_identifier.items():
        mask &= (df[col] == value)
    
    # Check if row exists
    if not mask.any():
        raise ValueError(f"No row found matching identifier: {row_identifier}")
    
    # Delete row
    return df[~mask].copy() 