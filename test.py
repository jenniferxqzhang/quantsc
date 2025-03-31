import pandas as pd
import re
from datetime import datetime

def parse_el_nino34_data_from_file(file_path):
    """
    Parse El Niño 3.4 region SST data from a text file into a pandas DataFrame.
    
    Parameters:
    file_path (str): Path to the text file containing El Niño SST data
    
    Returns:
    pandas.DataFrame: Parsed data with dates as index and Niño 3.4 SST values and anomalies
    """
    # Read the file content
    with open(file_path, 'r') as file:
        data_string = file.read()
    
    # Split the string into lines and remove empty lines
    lines = [line.strip() for line in data_string.split('\n') if line.strip()]
    
    # Create column names for Niño 3.4 region only
    column_names = ["Nino34_SST", "Nino34_SSTA"]
    
    # Create a list to hold the data
    data_rows = []
    
    # Pattern to match the date in format like "02SEP1981"
    date_pattern = re.compile(r'\d{2}[A-Z]{3}\d{4}')
    
    # Process each data row (starting from the 4th line, skipping headers)
    for line in lines[3:]:
        # Skip any lines that don't contain data
        if not date_pattern.search(line):
            continue
            
        # Split the line into parts
        parts = re.split(r'\s+', line.strip())
        
        # Extract the date
        date_str = parts[0]
        
        # Parse the date
        try:
            date = datetime.strptime(date_str, "%d%b%Y")
        except ValueError:
            # If there's an issue with the date format, keep it as a string
            date = date_str
        
        # In the data format, Niño 3.4 is the third region (after Niño1+2 and Niño3)
        # So we need to extract the 5th value (index 4 in 0-based indexing) if parts are separated
        if len(parts) >= 5:
            nino34_value = parts[4]
            
            # Use regex to separate SST and SSTA
            match = re.match(r'(\d+\.\d+)([-+]\d+\.\d+)', nino34_value)
            if match:
                sst = float(match.group(1))
                ssta = float(match.group(2))
                data_rows.append([date, sst, ssta])
    
    # Create a DataFrame from the data
    df = pd.DataFrame(data_rows, columns=['Date'] + column_names)
    
    # Set the date column as the index
    df.set_index('Date', inplace=True)
    
    return df

# Example usage
file_path = "/Users/jenniferzhang/Desktop/24_25/quantsc/noaa_elnino_data.txt"
df = parse_el_nino34_data_from_file(file_path)

# Display the DataFrame
print(df)

# You can also save the processed data to a CSV file if needed
# df.to_csv("nino34_data.csv")

# If you want to plot the data
import matplotlib.pyplot as plt

def plot_nino34_data(df):
    """
    Plot the Niño 3.4 SST and SSTA data.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with Niño 3.4 data
    """
    plt.figure(figsize=(12, 8))
    
    # Plot SST
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Nino34_SST'], 'b-', label='SST')
    plt.title('Niño 3.4 Sea Surface Temperature')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.legend()
    
    # Plot SSTA
    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['Nino34_SSTA'], 'r-', label='SSTA')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.title('Niño 3.4 Sea Surface Temperature Anomaly')
    plt.ylabel('Temperature Anomaly (°C)')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Uncomment the line below to plot the data
plot_nino34_data(df)

def calculate_statistics(df):
    """
    Calculate statistics for the Niño 3.4 SST and SSTA data.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with Niño 3.4 data
    
    Returns:
    dict: Dictionary containing mean, standard deviation, maximum, and minimum values
    """
    stats = {
        'Nino34_SST': {
            'mean': df['Nino34_SST'].mean(),
            'std': df['Nino34_SST'].std(),
            'max': df['Nino34_SST'].max(),
            'min': df['Nino34_SST'].min()  # Added min calculation
        },
        'Nino34_SSTA': {
            'mean': df['Nino34_SSTA'].mean(),
            'std': df['Nino34_SSTA'].std(),
            'max': df['Nino34_SSTA'].max(),
            'min': df['Nino34_SSTA'].min()  # Added min calculation
        }
    }
    
    return stats

# Calculate statistics and print in formatted way
statistics = calculate_statistics(df)
print("\n--- Statistics ---")
for key, value in statistics.items():
    print(f"{key}:")
    for stat, val in value.items():
        print(f"  {stat.capitalize()}: {val:.2f}")



