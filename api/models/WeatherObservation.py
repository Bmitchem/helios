import json
import base64
from datetime import datetime
from pydantic import BaseModel

from models.DatabaseModel import DatabaseModel


class WeatherObservation(DatabaseModel, BaseModel):
    """
    heatIndex, windChill and Temp are all strings because they include the scale in the value
    for example a heat index of 35 degrees Fahrenheit is recorded as 35f

    a future upgrade would be to pull these scales off and convert the value to Degrees Kelvin for storage
    then the value can be stored as a proper int, and converted to the appropriate scale during reporting
    """
    heatIndex: str
    windChill: str
    temp: str
    humidity: int
    obsTimeLocal: datetime
    stationId: str

    def serialize(self) -> str:
        return json.dumps({
            "pk": self.pk,
            "heatIndex": self.heatIndex,
            "windChill": self.windChill,
            "temp": self.temp,
            "humidity": self.humidity,
            "obsTimeLocal": self.obsTimeLocal.isoformat(),
            "stationId": self.stationId,
        })

    @property
    def pk(self):
        encoded = f'{self.obsTimeLocal.isoformat()}-{self.stationId}'.encode('utf-8')
        return f'{base64.b64encode(encoded).decode("ascii")}'

    def __str__(self):
        return f'WeatherObservation at time {self.obsTimeLocal} of temp {self.temp}'
