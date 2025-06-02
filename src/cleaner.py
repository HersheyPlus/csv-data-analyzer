import pandas as pd
import src.utils as utils

def filter_columns(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Filter dataframe to keep only specified columns.

    Args:
        df (pd.DataFrame): Original dataframe.
        columns (list, optional): List of columns to keep. Defaults to necessary columns.

    Returns:
        pd.DataFrame: Dataframe with only specified columns.
    """
    text:str = utils.split_and_join(columns, ", ")
    print(f"Filtering columns({len(columns)}): {text}")
    cols_to_keep = [col for col in columns if col in df.columns]
    return df[cols_to_keep]



def clean_data(df: pd.DataFrame, fill_na_cols=None, dropna_cols=None) -> pd.DataFrame:
    """
    Clean the input DataFrame by:
    - Dropping duplicate rows
    - Filling missing values in specified columns
    - Dropping rows with missing values in specified critical columns
    - Resetting index
    
    Args:
        df (pd.DataFrame): DataFrame after filtering.
        fill_na_cols (dict, optional): Dict of {col: fill_value} to fill missing values.
        dropna_cols (list, optional): List of critical columns to drop rows if missing.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.drop_duplicates()
    
    if fill_na_cols:
        for col, val in fill_na_cols.items():
            if col in df.columns:
                df[col].fillna(val, inplace=True)
    
    if dropna_cols:
        cols = [col for col in dropna_cols if col in df.columns]
        df = df.dropna(subset=cols)
    else:
        df = df.dropna()
        
    df = df.reset_index(drop=True)
    return df
