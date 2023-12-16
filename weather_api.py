import requests
import json
from datetime import datetime
from geopy.geocoders import Nominatim

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}

# def current_weather_apiwheather(city):
#     key = '3989965e44b440aa946124224230212'
#     # lat = "59.93"  # широта в градусах
#     # lon = "30.31"  # долгота в градусах
#     url = f"https://api.weatherapi.com/v1/current.json?key={key}&q={city}"
#     response = requests.get(url)  # отправление GET запроса и получение ответа от сервера
#     data = response.json()
#     # return response.json()
#     result = f'Город: {data["location"]["name"]}\n' \
#              f'Время получения данных о погоде: {datetime.fromisoformat(data["current"]["last_updated"]).time()}\n' \
#              f'Дата: {datetime.fromtimestamp(data["current"]["last_updated_epoch"]).date().strftime("%d/%m/%Y")}\n' \
#              f'Температура: {data["current"]["temp_c"]} C\n' \
#              f'Ощущается как: {data["current"]["feelslike_c"]} C\n' \
#              f'Состояние погоды: {data["current"]["condition"]["text"]}\n' \
#              f'Ветер: {data["current"]["wind_kph"]} км/ч\n' \
#              f'Влажность: {data["current"]["humidity"]}%\n'
#     return result


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    """
    geolocator = Nominatim(user_agent='my_test')
    location = geolocator.geocode(f'{lat}, {lon}')
    token = 'ff83a23e-d3d2-42f4-8930-f0693baf3711'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/informers??lat=59.93&lon=30.31"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    # return response.json()

    result = {
        'city': location.address, #"Санкт-Петербург", #data['geo_object']['locality']['name']
        'time': datetime.fromtimestamp(data['fact']['obs_time']).strftime("%H:%M"),
        'temp': data['fact']['temp'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['fact']['feels_like'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'pressure': data['fact']['pressure_mm'],  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['fact']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': data['fact']['wind_speed'],  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': data['fact']['wind_gust'],  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),
    }
    return result


if __name__ == "__main__":
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга

    # print(json.dumps(current_weather(lat, lon), indent=4, ensure_ascii=False))

    # city = input('Введи город: ')
    # print(current_weather_apiwheather(city))