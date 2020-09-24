import requests
from datetime import date


class Weather:
    def __init__(self, key, city):
        self.key = key
        self.city = city

    def current_weather(self):
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={self.key}&q={self.city}"
        response = requests.get(weather_url)
        data = response.json()

        res = {}

        if "error" in data:
            return None

        # Location details
        location = f"{data['location']['name']}, {data['location']['region']}"

        # Weather
        condition = data['current']['condition']
        desc, icon = condition['text'], "https:" + condition['icon']

        # Numbers
        degree = u"\N{DEGREE SIGN}"

        temp = data['current']
        current = f"{temp['temp_c']}{degree}C"
        wind = f"{temp['wind_kph']} kmph"
        pressure = f"{temp['pressure_mb']} mbar"
        feels_like = f"{temp['feelslike_c']}{degree}C"

        res = {'location': location, 'desc': desc, 'icon': icon, 'curr': current,
               'wind': wind, 'pressure': pressure, 'feels': feels_like}

        return res

    def astronomy(self):
        today = date.today()
        astro_url = f"https://api.weatherapi.com/v1/astronomy.json?key={self.key}&q={self.city}&dt={today}"
        response = requests.get(astro_url)
        data = response.json()

        if "error" in data:
            return None

        # Astronomy
        astro = data['astronomy']['astro']
        sunrise, sunset, moonrise, moonset = astro['sunrise'], astro[
            'sunset'], astro['moonrise'], astro['moonset']
        res = {'sunrise': sunrise, 'sunset': sunset,
               'moonrise': moonrise, 'moonset': moonset}

        return res
