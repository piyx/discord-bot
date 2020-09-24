import requests
from .secret import NASA_API

# Astronomy picture of day


def apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API}"
    response = requests.get(url)
    if not response.ok:
        return None

    data = response.json()
    info = data['explanation']
    img = data['url']
    return info, img
