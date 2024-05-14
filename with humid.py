import requests # api requests
import pandas as pd # for data processing
import matplotlib.pyplot as plt # for making graphs
from geopy.geocoders import Nominatim # determine the coordinates of Toronto
from datetime import datetime, timedelta  # delta between datas
from matplotlib.dates import DayLocator

# Set parameters for hourly weather data request
url = "https://meteostat.p.rapidapi.com/point/hourly" # use url with hourly data for humidity

# Geocode the city name to get its coordinates
geolocator = Nominatim(user_agent="toronto_weather") # initializing an object to determine coordinates by place name
location = geolocator.geocode("Toronto") # getting the coordinates of toronto / can change the city
latitude = location.latitude # getting the lat
longitude = location.longitude # getting the lon

# Calculate the start date as one month ago from today
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d") # getting the date of starting period and
# transform for normal format

# Set end date as today
end_date = datetime.now().strftime("%Y-%m-%d") # put the today data how the start point

# Set request parameters: location (latitude and longitude), station identifier, and time period
params = {
    'lat': latitude,  # Latitude of Toronto
    'lon': longitude,  # Longitude of Toronto
    'start': start_date,
    'end': end_date
}

headers = {
    'X-RapidAPI-Key': 'cddc899bd3msh4bc5e924d0cebfcp10326ejsn7d41e15879bd', # my api key from meteostat
    'X-RapidAPI-Host': 'meteostat.p.rapidapi.com'
}

try:
    # Perform the request
    response = requests.get(url, headers=headers, params=params) # perform a request for weather data

    # Check the response status code
    if response.status_code == 200:
        # Get hourly weather data
        hourly_weather_data = response.json()['data'] # extract hourly weather data from response

        # Convert data to DataFrame
        hourly_df = pd.DataFrame(hourly_weather_data) # creating a DataFrame object to process the data

        # Convert 'time' column to datetime format
        hourly_df['time'] = pd.to_datetime(hourly_df['time']) # conversion for ease of reading and operation
        # Эта строка создает новый столбец 'time', в котором каждое значение преобразуется из исходного формата в
        # формат даты и времени. После выполнения этой операции мы можем выполнять различные операции с временными
        # данными, такие как фильтрация по датам, агрегация по времени и создание временных рядов.

        # Extract date from time
        hourly_df['date'] = hourly_df['time'].dt.date # converts to date without time

        # Aggregate data by day
        daily_df = hourly_df.groupby('date').agg({
            'temp': 'mean',  # Average temperature per day
            'rhum': 'mean',  # Average humidity per day
            'pres': 'mean'  # Average pressure per day
        }).reset_index() # resetting the grouping index and returning it as a regular numeric index.

        # Rename columns
        daily_df.rename(columns={
            'date': 'Date',
            'temp': 'Temperature (°C)',
            'rhum': 'Humidity (%)',
            'pres': 'Pressure (hPa)'
        }, inplace=True) # the changes will be applied to the DF object itself rather than creating a new
        # DF with renamed columns

        # Plot the data
        plt.figure(figsize=(10, 6)) # the size
        plt.plot(daily_df['Date'], daily_df['Temperature (°C)'], marker='o', linestyle='-', label='Average Temperature')
        plt.plot(daily_df['Date'], daily_df['Humidity (%)'], marker='o', linestyle='-', label='Average Humidity')
        plt.plot(daily_df['Date'], daily_df['Pressure (hPa)'], marker='o', linestyle='-', label='Average Pressure')
        plt.xlabel('Date') # name 'x' axis
        plt.ylabel('Values') # name 'y' axis
        plt.title('Weather Trends in Toronto') # title of the graph
        plt.legend() # display the legend
        plt.grid(True) # display the grid
        plt.xticks(rotation=45) # turn the date for 45 degree
        plt.gca().xaxis.set_major_locator(DayLocator()) # on the 'x' axis dates for every day
        plt.tight_layout() # leveling
        plt.show()

        # Write data to an Excel file with renamed columns
        daily_df.to_excel('toronto_weather_data_with_humid.xlsx', index=False) # data without index of line

    else:
        print("Error retrieving weather data:")
        print(response.text)
except Exception as e:
    print("An error occurred while executing the request:")
    print(e)
