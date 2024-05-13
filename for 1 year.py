import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from geopy.geocoders import Nominatim # installed geopy by pip
from matplotlib.dates import MonthLocator

# Define the current date
current_date = datetime.datetime.now()

# Define the date of last year
last_year_date = current_date - datetime.timedelta(days=365)

# Geocode the city name to get its coordinates
geolocator = Nominatim(user_agent="toronto_weather")
location = geolocator.geocode("Toronto")
latitude = location.latitude
longitude = location.longitude

# Set the request parameters to get the nearest station to Toronto
url = "https://meteostat.p.rapidapi.com/stations/nearby"
params = {
    'lat': latitude,
    'lon': longitude
}
headers = {
    'X-RapidAPI-Key': 'cddc899bd3msh4bc5e924d0cebfcp10326ejsn7d41e15879bd',
    'X-RapidAPI-Host': 'meteostat.p.rapidapi.com'
}

# Perform the request to get the nearest stations
try:
    response = requests.get(url, headers=headers, params=params)
    # Check the response status code
    if response.status_code == 200:
        # Get the identifier of the nearest station from the response
        station_id = response.json()['data'][0]['id'] # dictionary for meteo station

        # Convert dates to the required format (YYYY-MM-DD)
        start_date = last_year_date.strftime("%Y-%m-%d") # change the date format
        end_date = current_date.strftime("%Y-%m-%d")

        # Now make a request to get daily weather data for a year
        url = f"https://meteostat.p.rapidapi.com/stations/daily?station={station_id}"
        params = {
            'start': start_date,
            'end': end_date
        }

        # Perform the request
        response = requests.get(url, headers=headers, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Get the weather data
            weather_data = response.json()['data']

            # Create a DataFrame object with the weather data
            df = pd.DataFrame(weather_data)

            # Select only the columns for date, average temperature and pressure
            df = df[['date', 'tavg', 'pres']]

            # Rename the columns for clarity
            df.columns = ['Date', 'Average Temperature (°C)', 'Pressure']

            # Plot the graph
            plt.figure(figsize=(10, 6)) # create a graph 10x6 du
            plt.plot(df['Date'], df['Average Temperature (°C)'], marker='o') # use date for 'x' and temp for 'y'
            plt.xlabel('Date') # name 'x'
            plt.ylabel('Average Temperature (°C)') # name 'y'
            plt.title('Average Temperature in Toronto (Year from Today to Last Year)') # name of the graph
            plt.gca().xaxis.set_major_locator(MonthLocator())  # set ticks for each month
            plt.xticks(rotation=45) # turn the gate on 'x'
            plt.grid(True) # turn on the grid on the chart
            plt.tight_layout() # automatic alignment of graph elements for better display
            plt.show()

            # Write data to an Excel file
            df.to_excel('toronto_weather_data.xlsx', index=False)

        else:
            print("Error fetching weather data:") # ошибка данных о получении погоды
            print(response.text)
    else:
        print("Error fetching nearest stations:") # ошибка о станции
        print(response.text)
except Exception as e:
    print("An error occurred while executing the request:") # ошибка в целом о реквесте
    print(e)
