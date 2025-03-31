import pandas as pd
import os

# --- 1. SET FILE PATH ---
file_path = "/Users/jenniferzhang/Desktop/24_25/quantsc/noaa_elnino_data.txt"

# --- 2. FILE PATH DEBUGGING ---
print("--- File Path Debugging ---")
print("File Path:", file_path)

if not os.path.exists(file_path):
    print("ERROR: File does NOT exist!")
    print("Files in directory:")
    try:
        print(os.listdir(os.path.dirname(file_path)))
    except FileNotFoundError:
        print("ERROR: Directory does not exist either!")
    exit()
else:
    print("File exists. Proceeding...")

# --- 3. READ THE DATA ---
try:
    df = pd.read_csv(
        file_path,
        sep="\s+",
        header=1,
        na_values="-99.99",
        engine='python'
    )

    # Rename the first column to 'Week'
    df = df.rename(columns={df.columns[0]: 'Week'})
    print("\n--- Raw Data (First 5 Rows) ---")
    print(df.head())
    print("\n--- Data Shape (Rows, Columns) ---")
    print(df.shape)

except Exception as e:
    print(f"\nERROR reading file: {e}")
    exit()

# --- 4. DATA CLEANING & EXTRACTION ---
df = df.dropna()
try:
    # Reset index so 'Week' is a column
    df = df.reset_index()

    # Extract year from 'Week' and create 'Year' column
    df['Year'] = df['Week'].str[-4:].astype(int)

    # Extract month from 'Week' and create 'Month' column
    df['Month'] = df['Week'].str[2:5]
    month_map = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
    df['Month'] = df['Month'].map(month_map)

    # Extract day from 'Week'
    df['Day'] = df['Week'].str[:2].astype(int)

    # Create 'Date' column
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.set_index('Date')
    
    # Extract El Nino 34 SST and SSTA.  Handles 'None' values correctly.
    def extract_sst_ssta(value):
        if isinstance(value, str):  # Check if the value is a string
            parts = value.split('-')
            return float(parts[0]), float(parts[1])
        return None, None  # Return None, None for non-string values

    df['Nino34_SST'], df['Nino34_SSTA'] = zip(*df['Nino34'].apply(extract_sst_ssta))
    
    # Create a new DataFrame with the desired columns
    data = df[['Week',  'Nino34_SST', 'Nino34_SSTA']].copy()
    
    print("\n--- Cleaned Data (First 5 Rows) ---")
    print(data.head())
    print("\n--- Cleaned Data Info ---")
    print(data.info())

except (IndexError, KeyError) as e:
    print(f"ERROR processing data: {e}")
    exit()
except ValueError as e:
    print(f"ERROR processing dates: {e}")
    exit()
