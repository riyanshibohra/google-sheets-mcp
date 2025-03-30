import pandas as pd
from typing import Dict, Any

def add_data(df_json: str, row_data: Dict[str, Any]) -> str:
    """Add a new row to the dataset"""
    # Convert JSON string to DataFrame
    df = pd.read_json(df_json, orient='split')
    
    # Validate that all columns exist
    if not all(col in df.columns for col in row_data.keys()):
        invalid_cols = [col for col in row_data.keys() if col not in df.columns]
        raise ValueError(f"Invalid columns: {invalid_cols}")
    
    # Add new row using concat
    new_df = pd.DataFrame([row_data])
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Return updated DataFrame as JSON
    return df.to_json(orient='split')

def edit_data(df_json: str, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> str:
    """Edit an existing row"""
    # Convert JSON string to DataFrame
    df = pd.read_json(df_json, orient='split')
    
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
    for field, value in updated_data.items():
        df.loc[mask, field] = value
    
    # Return updated DataFrame as JSON
    return df.to_json(orient='split')

def delete_data(df_json: str, row_identifier: Dict[str, Any]) -> str:
    """Delete a row"""
    # Convert JSON string to DataFrame
    df = pd.read_json(df_json, orient='split')
    
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
    df = df[~mask]
    
    # Return updated DataFrame as JSON
    return df.to_json(orient='split') 