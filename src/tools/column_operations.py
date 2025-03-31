import pandas as pd
from typing import Dict, List

def add_column(df: pd.DataFrame, new_column_name: str, formula: str, reference_columns: List[str], params: Dict = None) -> pd.DataFrame:
    """Add a new column based on calculations from other columns.
    
    Args:
        df: Input DataFrame
        new_column_name: Name for the new column
        formula: Operation type ('concat', 'sum', 'multiply', 'divide', 'subtract')
        reference_columns: Columns to use in calculation
        params: Optional parameters for string operations (separator, prefix, suffix, format_string)
    """
    df_copy = df.copy()
    params = params or {}
    
    # Validate columns
    invalid_cols = [col for col in reference_columns if col not in df_copy.columns]
    if invalid_cols:
        raise ValueError(f"Invalid reference columns: {invalid_cols}")
    if new_column_name in df_copy.columns:
        raise ValueError(f"Column '{new_column_name}' already exists")
    
    # Apply formula
    if formula == 'concat':
        separator = str(params.get('separator', ' '))
        prefix = str(params.get('prefix', ''))
        suffix = str(params.get('suffix', ''))
        format_string = params.get('format_string', None)
        
        if format_string:
            df_copy[new_column_name] = df_copy[reference_columns].apply(
                lambda row: format_string.format(*[str(val) for val in row]), axis=1
            )
        else:
            values = df_copy[reference_columns].astype(str).apply(
                lambda row: separator.join(row.values.astype(str)), axis=1
            )
            df_copy[new_column_name] = prefix + values + suffix
            
    elif formula == 'sum':
        df_copy[new_column_name] = df_copy[reference_columns].sum(axis=1)
    elif formula == 'multiply':
        df_copy[new_column_name] = df_copy[reference_columns].prod(axis=1)
    elif formula in ['divide', 'subtract']:
        if len(reference_columns) != 2:
            raise ValueError(f"{formula.title()} requires exactly 2 reference columns")
        if formula == 'divide':
            df_copy[new_column_name] = df_copy[reference_columns[0]] / df_copy[reference_columns[1]]
        else:
            df_copy[new_column_name] = df_copy[reference_columns[0]] - df_copy[reference_columns[1]]
    else:
        raise ValueError(f"Unsupported formula: {formula}")
    
    return df_copy

def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """Rename a column in the DataFrame."""
    df_copy = df.copy()
    
    if old_name not in df_copy.columns:
        raise ValueError(f"Column '{old_name}' not found")
    if new_name in df_copy.columns:
        raise ValueError(f"Column '{new_name}' already exists")
    
    return df_copy.rename(columns={old_name: new_name})

def transform_column(df: pd.DataFrame, column_name: str, transformation: str, params: Dict = None) -> pd.DataFrame:
    """Transform values in a column using various operations.
    
    Args:
        df: Input DataFrame
        column_name: Column to transform
        transformation: Type ('uppercase', 'lowercase', 'title_case', 'round', 'format_date')
        params: Optional parameters (split_on, part_index, decimals, format)
    """
    df_copy = df.copy()
    params = params or {}
    
    if column_name not in df_copy.columns:
        raise ValueError(f"Column '{column_name}' not found")
    
    if transformation == 'uppercase':
        df_copy[column_name] = df_copy[column_name].astype(str).str.upper()
    elif transformation == 'lowercase':
        df_copy[column_name] = df_copy[column_name].astype(str).str.lower()
    elif transformation == 'title_case':
        split_on = params.get('split_on', None)
        part_index = params.get('part_index', -1)
        
        if split_on:
            def title_case_part(text):
                parts = text.split(split_on)
                if 0 <= part_index < len(parts):
                    parts[part_index] = parts[part_index].strip().title()
                return split_on.join(parts)
            df_copy[column_name] = df_copy[column_name].astype(str).apply(title_case_part)
        else:
            df_copy[column_name] = df_copy[column_name].astype(str).str.title()
    elif transformation == 'round':
        df_copy[column_name] = df_copy[column_name].round(params.get('decimals', 0))
    elif transformation == 'format_date':
        df_copy[column_name] = pd.to_datetime(df_copy[column_name]).dt.strftime(
            params.get('format', '%Y-%m-%d')
        )
    else:
        raise ValueError(f"Unsupported transformation: {transformation}")
    
    return df_copy 