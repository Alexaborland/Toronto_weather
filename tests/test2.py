import requests
import pandas as pd
import datetime

# Замените 'YOUR_API_KEY' на ваш API ключ OpenWeather
API_KEY = '8f5817ef9a00ff8ec592b6a9518cd12a'

# Определите текущую дату
current_date = datetime.datetime.now()

# Определите дату прошлого года
last_year_date = current_date - datetime.timedelta(days=365)

# Установите параметры запроса для получения погодных данных от OpenWeather API
url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
params = {
    'lat': '43.65107',  # Широта Торонто
    'lon': '-79.347015',  # Долгота Торонто
    'appid': API_KEY
}

# Создайте пустой список для хранения данных о погоде
weather_data = []

# Итерируемся по дням за последний год и делаем запросы к OpenWeather API
current_date = last_year_date
while current_date <= datetime.datetime.now():
    timestamp = int(current_date.timestamp())
    params['dt'] = timestamp
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Получаем данные о средней температуре, влажности и давлении
        avg_temp = data['current']['temp'] - 273.15  # переводим из Кельвинов в Цельсии
        humidity = data['current']['humidity']
        pressure = data['current']['pressure']
        # Добавляем данные в список
        weather_data.append({
            'Date': current_date.strftime("%Y-%m-%d"),
            'Average Temperature (°C)': avg_temp,
            'Average Humidity (%)': humidity,
            'Average Pressure (hPa)': pressure
        })
    # Увеличиваем текущую дату на один день
    current_date += datetime.timedelta(days=1)

# Создаем DataFrame из полученных данных о погоде
df = pd.DataFrame(weather_data)

# Записываем данные в файл Excel
df.to_excel('toronto_weather_data.xlsx', index=False)

print("Данные успешно записаны в файл toronto_weather_data.xlsx")
