import base64
import datetime
import logging

import requests

from constants import WEATHER_API_KEY
from models.db import Database
logger = logging.getLogger(__name__)

def roundToNearestFiveMinutes(date: datetime.datetime) -> datetime:
    # in those instances where the minutes are already at target
    delta = date.minute % 5
    return datetime.datetime(
        date.year,
        date.month,
        date.day,
        date.hour,
        date.minute - delta,
        0, # Seconds
        0  # MS
    )

def convertFtoK(temp: int) -> float:
    kelvinTemp = (temp - 32) * (5 / 9) + 273.15
    return format(kelvinTemp, '.2f')
# (273.15K − 273.15) × 9/5 + 32 = 32°F
def convertKelvinToFahrenheit(kelvinTemp: float) -> str:
    fahrenheitTemp = (kelvinTemp - 273.15) * (9 / 5) + 32
    return format(fahrenheitTemp, '.2f')

# 373.15K − 273.15 = 100°C
def convertKelvinToCelsius(kelvinTemp: float) -> str:
    celsiusTemp = (kelvinTemp - 273.15)
    return format(celsiusTemp, '.2f')

def fetchWeatherObservation(stationId: str):
    REQUEST_URL = f'https://api.weather.com/v2/pws/observations/current?stationId={stationId}&format=json&units=e&apiKey={WEATHER_API_KEY}'
    response = requests.get(REQUEST_URL)
    if response.ok:
        payload = response.json()
        observation = payload['observations'][0]

        data = {
            'heatIndex': convertFtoK(observation['imperial']['heatIndex']),
            'windChill': convertFtoK(observation['imperial']['windChill']),
            'temp': convertFtoK(observation['imperial']['temp']),
            'humidity': observation['humidity'],
            "obsTimeLocal": observation['obsTimeLocal'],
            "stationId": observation['stationID']
        }
        return data
    else:
        logger.error(response.text)

def listWeatherStations():
    db = Database()
    results = db.search('weather-station', [])
    return results

def computeWeatherObservationPK(dateOfObservation: datetime, stationId: str) -> str:
    encoded = f'{dateOfObservation.isoformat()}-{stationId}'.encode('utf-8')
    return f'weather-observation-{base64.b64encode(encoded).decode("ascii")}'