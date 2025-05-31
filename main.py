from src.loader import load_data_csv
from src.cleaner import clean_data, filter_columns

df = load_data_csv('ginf.csv')
columns_to_keep = ['id_odsp', 'date', 'league', 'season', 'ht', 'at', 'fthg', 'ftag']
df_filtered = filter_columns(df, columns_to_keep)

df_cleaned = clean_data(
    df_filtered
)
print("Original data shape:", df.shape)
print("Filtered and cleaned data shape:", df_cleaned.shape)