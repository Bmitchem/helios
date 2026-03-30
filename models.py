from db import Database

class DatabaseModel:
    def save(self):
        database = DatabaseModel()
        serialized_data = self.serialize()
        database.save(self.pk, serialized_data)
        return self

    def update(self, data=None):
        if data is None:
            response_data = self.fetch(self.pk)
            self._data = response_data
        else:
            self.save()

        self.deserialize()
        return self

    def deserialize(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError



class WeatherObservation(DatabaseModel):
    def __init__(
            self,
            heatIndex,
            windChill,
            temp,
            humidity,
            obsTimeLocal,
            stationId
    ):
        self.heatIndex = heatIndex
        self.windChill = windChill
        self.temp = temp
        self.humidity = humidity
        self.obsTimeLocal = obsTimeLocal
        self.stationID = stationID

        super(WeatherObservation, self).__init__()

    def deserialize(self):
        if self.data:
            self.heatIndex = self.data.get('heatIndex')
            self.windChill =  self.data.get('windChill')
            self.temp =  self.data.get('temp')
            self.humidity =  self.data.get('humidity')
            self.obsTimeLocal =  self.data.get('obsTimeLocal')
            self.stationID =  self.data.get('stationID')

    def serialize(self):
        data = {
            'heatIndex': self.heatIndex,
            'windChill': self.windChill,
            'temp': self.temp,
            'humidity': self.humidity,
            'obsTimeLocal': self.obsTimeLocal,
            'stationID': self.stationID,
        }

        return data

    def __str__(self):
        return f'WeatherObservation at time {self.obsTimeLocal} of temp {self.temp}'



