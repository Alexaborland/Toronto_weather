import requests
import pandas as pd
import matplotlib.pyplot as plt

# Установите параметры запроса для получения ближайшей станции к Торонто
url = "https://meteostat.p.rapidapi.com/stations/nearby"
params = {
    'lat': '43.65107',  # Широта Торонто
    'lon': '-79.347015'  # Долгота Торонто
}
headers = {
    'X-RapidAPI-Key': 'cddc899bd3msh4bc5e924d0cebfcp10326ejsn7d41e15879bd',
    'X-RapidAPI-Host': 'meteostat.p.rapidapi.com'
}

# Выполните запрос, чтобы получить ближайшие станции
try:
    response = requests.get(url, headers=headers, params=params)
    # Проверяем статус кода ответа
    if response.status_code == 200:
        # Получаем идентификатор ближайшей станции из ответа
        station_id = response.json()['data'][0]['id']

        # Теперь делаем запрос на получение ежедневных данных о погоде с 1 по 8 мая 2024 года для Торонто
        url = f"https://meteostat.p.rapidapi.com/stations/daily?station={station_id}"
        params = {
            'start': '2023-05-08',
            'end': '2024-05-08'
        }

        # Выполните запрос
        response = requests.get(url, headers=headers, params=params)

        # Проверяем статус кода ответа
        if response.status_code == 200:
            # Получаем данные о погоде
            weather_data = response.json()['data']

            # Создаем DataFrame с данными о погоде
            df = pd.DataFrame(weather_data)

            # Извлекаем данные о дате и средней температуре из ответа
            dates = df['date']
            avg_temperatures = df['tavg']

            # Строим график
            plt.figure(figsize=(10, 6))
            plt.plot(dates, avg_temperatures, marker='o', linestyle='-')
            plt.xlabel('Date')
            plt.ylabel('Average Temperature (°C)')
            plt.title('Average Temperature in Toronto (May 1-8, 2024)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            # Записываем данные в файл Excel
            df.to_excel('toronto_weather_data.xlsx', index=False)

        else:
            print("Ошибка при запросе данных о погоде:")
            print(response.text)
    else:
        print("Ошибка при запросе ближайших станций:")
        print(response.text)
except Exception as e:
    print("Произошла ошибка при выполнении запроса:")
    print(e)
