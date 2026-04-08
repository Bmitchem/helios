from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from tasks.celery import save_station


class WeatherStation(BaseModel):
    stationId: str
    stationName: str
    lastUpdatedTimestamp: Optional[datetime] = None

    def serialize(self) -> dict:
        return {
            'stationId': self.stationId,
            'stationName': self.stationName,
            'lastUpdatedTimestamp': self.lastUpdatedTimestamp
        }

    @property
    def pk(self):
        return self.compute_pk(stationId=self.stationId)

    @staticmethod
    def compute_pk(stationId: str) -> str:
        return f'weather-station-{stationId}'

    def save(self):
        save_station(self.pk, self.serialize())