import json
import requests
import os
from datetime import datetime
from secret import APIKEY

# city = input("Enter city: ")


def show(city):
    from datetime import datetime
    # Location
    API_KEY = APIKEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(url)

    weather = response.json()
    KELVIN = 273.15
    degree = u"\N{DEGREE SIGN}"
    ds = {}
    if "message" in weather:
        ds['message'] = weather["message"]
    else:
        ds['Weather'] = weather['weather'][0]['main']
        ds['Description'] = weather['weather'][0]['description']
        ds['Max temp'] = str(
            round(weather['main']['temp_max'] - KELVIN)) + f'{degree}C'
        ds['Min temp'] = str(
            round(weather['main']['temp_min'] - KELVIN)) + f'{degree}C'
        ds['Sunrise'] = str(datetime.fromtimestamp(
            weather['sys']['sunrise'])).split(" ")[-1]
        ds['Sunset'] = str(datetime.fromtimestamp(
            weather['sys']['sunset'])).split(" ")[-1]
    return ds
