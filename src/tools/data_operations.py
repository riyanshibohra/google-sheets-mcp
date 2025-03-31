import pandas as pd
from typing import Dict, Any

def add_data(df: pd.DataFrame, row_data: Dict[str, Any]) -> pd.DataFrame:
    """Add a new row to the dataset.
    
    Args:
        df: Input DataFrame
        row_data: Dictionary with column names and values for the new row
    """
    # Validate columns
    invalid_cols = [col for col in row_data.keys() if col not in df.columns]
    if invalid_cols:
        raise ValueError(f"Invalid columns: {invalid_cols}")
    
    return pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)

def edit_data(df: pd.DataFrame, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> pd.DataFrame:
    """Edit an existing row in the dataset.
    
    Args:
        df: Input DataFrame
        row_identifier: Dictionary to identify the row (e.g., {"name": "John"})
        updated_data: Dictionary with column names and new values
    """
    df_copy = df.copy()
    
    # Validate columns
    for cols, name in [(row_identifier, 'identifier'), (updated_data, 'update')]:
        invalid = [col for col in cols.keys() if col not in df.columns]
        if invalid:
            raise ValueError(f"Invalid {name} columns: {invalid}")
    
    # Find and update row
    mask = pd.Series(True, index=df.index)
    for col, value in row_identifier.items():
        mask &= (df[col] == value)
    
    if not mask.any():
        raise ValueError(f"No row found matching identifier: {row_identifier}")
    
    for field, value in updated_data.items():
        df_copy.loc[mask, field] = value
    
    return df_copy

def delete_data(df: pd.DataFrame, row_identifier: Dict[str, Any]) -> pd.DataFrame:
    """Delete a row from the dataset.
    
    Args:
        df: Input DataFrame
        row_identifier: Dictionary to identify the row to delete
    """
    # Validate columns
    invalid_cols = [col for col in row_identifier.keys() if col not in df.columns]
    if invalid_cols:
        raise ValueError(f"Invalid identifier columns: {invalid_cols}")
    
    # Find row
    mask = pd.Series(True, index=df.index)
    for col, value in row_identifier.items():
        mask &= (df[col] == value)
    
    if not mask.any():
        raise ValueError(f"No row found matching identifier: {row_identifier}")
    
    return df[~mask].copy() 