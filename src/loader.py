import os
import pandas as pd
import src.utils as utils

def load_data_csv(file_name: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    file_path = os.path.join(base_path, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)
    
    print(f"Loaded '{file_name}' successfully!")
    print(f"Total rows: {df.shape[0]}")
    print(f"Total columns: {df.shape[1]}")
    print(f"Columns: {utils.split_and_join(df.columns.tolist())}\n",)
    
    return df
