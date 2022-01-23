import os
import json
from requests import get
from dotenv import load_dotenv

key = os.getenv('openWeather')

def weather(city: str) -> dict:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric'
    data = json.loads(get(url).content)
    return data
