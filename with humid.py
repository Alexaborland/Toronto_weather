import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set parameters for hourly weather data request
url = "https://meteostat.p.rapidapi.com/point/hourly"

# Set request parameters: location (latitude and longitude), station identifier, and time period
params = {
    'lat': '43.65107',  # Latitude of Toronto
    'lon': '-79.347015',  # Longitude of Toronto
    'start': '2024-04-08',
    'end': '2024-05-08',
    'station': '71624'  # Identifier of the nearest station
}

headers = {
    'X-RapidAPI-Key': 'cddc899bd3msh4bc5e924d0cebfcp10326ejsn7d41e15879bd',
    'X-RapidAPI-Host': 'meteostat.p.rapidapi.com'
}

try:
    # Perform the request
    response = requests.get(url, headers=headers, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Get hourly weather data
        hourly_weather_data = response.json()['data']

        # Convert data to DataFrame
        hourly_df = pd.DataFrame(hourly_weather_data)

        # Convert 'time' column to datetime format
        hourly_df['time'] = pd.to_datetime(hourly_df['time'])

        # Extract date from time
        hourly_df['date'] = hourly_df['time'].dt.date

        # Aggregate data by day
        daily_df = hourly_df.groupby('date').agg({
            'temp': 'mean',  # Average temperature per day
            'rhum': 'mean',  # Average humidity per day
            'pres': 'mean'  # Average pressure per day
        }).reset_index()

        # Rename columns
        daily_df.rename(columns={
            'date': 'Date',
            'temp': 'Temperature (°C)',
            'rhum': 'Humidity (%)',
            'pres': 'Pressure (hPa)'
        }, inplace=True)

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(daily_df['Date'], daily_df['Temperature (°C)'], marker='o', linestyle='-', label='Average Temperature')
        plt.plot(daily_df['Date'], daily_df['Humidity (%)'], marker='s', linestyle='--', label='Average Humidity')
        plt.plot(daily_df['Date'], daily_df['Pressure (hPa)'], marker='^', linestyle=':', label='Average Pressure')
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title('Weather Trends in Toronto')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Write data to an Excel file with renamed columns
        daily_df.to_excel('toronto_weather_data_with_humid.xlsx', index=False)

    else:
        print("Error retrieving weather data:")
        print(response.text)
except Exception as e:
    print("An error occurred while executing the request:")
    print(e)
