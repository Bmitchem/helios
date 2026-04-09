import base64
import logging
from datetime import datetime
from pydantic import BaseModel

from models.db import Database
from models.utils import roundToNearestFiveMinutes, convertKelvinToFahrenheit, convertKelvinToCelsius, convertFtoK, \
    fetchWeatherObservation

logger = logging.getLogger(__name__)

class WeatherObservation(BaseModel):
    """
    heatIndex, windChill and Temp are all strings because they include the scale in the value
    for example a heat index of 35 degrees Fahrenheit is recorded as 35f

    a future upgrade would be to pull these scales off and convert the value to Degrees Kelvin for storage
    then the value can be stored as a proper int, and converted to the appropriate scale during reporting
    """
    heatIndex: float
    windChill: float
    temp: float
    humidity: int
    obsTimeLocal: datetime
    stationId: str

    def serialize(self) -> dict:
        return {
            "pk": self.pk,
            "heatIndex": self.heatIndex,
            "windChill": self.windChill,
            "temp": self.temp,
            "humidity": self.humidity,
            "obsTimeLocal": roundToNearestFiveMinutes(self.obsTimeLocal).isoformat(),
            "stationId": self.stationId,
        }

    @property
    def pk(self):
        return self.compute_pk(self.obsTimeLocal, self.stationId)

    @staticmethod
    def compute_pk(dateOfObservation: datetime, stationId: str) -> str:
        encoded = f'{dateOfObservation.isoformat()}-{stationId}'.encode('utf-8')
        return f'weather-observation-{base64.b64encode(encoded).decode("ascii")}'


    @staticmethod
    def getOrCreateObservation(stationId: str) -> dict:
        logging.info(f'Running WeatherObservation.getOrCreateObservation for stationId => {stationId}')
        nearestObs = roundToNearestFiveMinutes(datetime.now())
        pk = WeatherObservation.compute_pk(nearestObs, stationId)

        db = Database()
        existingDocument = db.fetch(pk)
        if existingDocument:
            logging.info(f'Document exists in cache, returning cached version ({pk})')
            return existingDocument

        # else:
        logging.info(f'Document not in cache, fetching ({pk})')
        observation = WeatherObservation.fetchObservation(stationId)
        serializedData = observation.serialize()
        logging.info(f'Saving cached document({pk})')
        from tasks.celery import save_observation
        save_observation.s(pk, serializedData)
        return serializedData

    @staticmethod
    def fetchObservation(stationId: str):
        data = fetchWeatherObservation(stationId)
        return WeatherObservation(**data)

    @staticmethod
    def localize(observation: dict, unit: str) -> dict:
        if unit == 'imperial':
            observation['heatIndex'] = f"{convertKelvinToFahrenheit(observation['heatIndex'])}f"
            observation['windChill'] = f"{convertKelvinToFahrenheit(observation['windChill'])}f"
            observation['temp'] = f"{convertKelvinToFahrenheit(observation['temp'])}f"
        elif unit == 'metric':
            observation['heatIndex'] = f"{convertKelvinToCelsius(observation['heatIndex'])}c"
            observation['windChill'] = f"{convertKelvinToCelsius(observation['windChill'])}c"
            observation['temp'] = f"{convertKelvinToCelsius(observation['temp'])}c"
        else: # Default is kelvin
            observation['heatIndex'] = f"{observation['heatIndex']:.0f}k"
            observation['windChill'] = f"{observation['windChill']:.0f}k"
            observation['temp'] = f"{observation['temp']:.0f}k"
        return observation


    def __str__(self):
        return f'WeatherObservation at time {self.obsTimeLocal} of temp {self.temp}'
