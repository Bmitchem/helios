from datetime import datetime

from pydantic import BaseModel

from models.models import DatabaseModel


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

    # def __init__(
    #         self,
    #         heatIndex,
    #         windChill,
    #         temp,
    #         humidity,
    #         obsTimeLocal,
    #         stationId
    # ):
    #     self.heatIndex = heatIndex
    #     self.windChill = windChill
    #     self.temp = temp
    #     self.humidity = humidity
    #     self.obsTimeLocal = obsTimeLocal
    #     self.stationId = stationId
    #     super(WeatherObservation, self).__init__()
    #
    # def validate(self):
    #     return self.model_validate(self.serialize())
    #
    # def deserialize(self):
    #     if self.data:
    #         self.heatIndex = self.data.get('heatIndex')
    #         self.windChill =  self.data.get('windChill')
    #         self.temp =  self.data.get('temp')
    #         self.humidity =  self.data.get('humidity')
    #         self.obsTimeLocal =  self.data.get('obsTimeLocal')
    #         self.stationID =  self.data.get('stationID')
    #
    # def serialize(self):
    #     data = {
    #         'heatIndex': self.heatIndex,
    #         'windChill': self.windChill,
    #         'temp': self.temp,
    #         'humidity': self.humidity,
    #         'obsTimeLocal': self.obsTimeLocal,
    #         'stationID': self.stationID,
    #     }
    #
    #     return data

    def __str__(self):
        return f'WeatherObservation at time {self.obsTimeLocal} of temp {self.temp}'
