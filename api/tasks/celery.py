import os
import logging
from celery import Celery


from models.db import Database
from models.utils import listWeatherStations

logger = logging.getLogger(__name__)
REDIS_HOST=os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT=os.environ.get("REDIS_PORT", "6379")
WEATHER_QUERY_FREQUENCY = 60 * 5 # 5 minutes

print(f'connecting to redis at: {REDIS_HOST}:{REDIS_PORT}')

app = Celery(
    'tasks',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # broker=f'{REDIS_HOST}:{REDIS_PORT}/0',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # backend=f'{REDIS_HOST}:{REDIS_PORT}/0',
    # include=['celery.tasks']
)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        WEATHER_QUERY_FREQUENCY,
        update_station_observations.s(),
        name="refresh weather from saved stations"
    )

@app.task(name='tasks.hello')
def hello():
    with open('task_output.txt', 'w') as f:
        f.write('Hello World')

    return 'Hello World!'

@app.task(name='tasks.save_observation')
def save_observation(pk: str, observation: str):
    logger.info(f'Saving observation to pk {pk}')
    db = Database()
    db.save(pk, observation)
    return pk

@app.task(name='tasks.save_station')
def save_station(pk: str, station: str):
    db = Database()
    db.save(pk, station)
    return pk

@app.task(name='tasks.query_weather')
def query_weather(station_id: str):
    from models.WeatherObservation import WeatherObservation
    logger.info(f'Quering weather station: {station_id}')
    observation = WeatherObservation.fetchObservation(station_id)
    serializedData = observation.serialize()
    save_observation.s(observation.pk, serializedData)

@app.task(name='tasks.update_station_observations')
def update_station_observations():
    logger.info(f'Querying weather stations')
    stations = listWeatherStations()
    stationIds = [station['stationId'] for station in stations]
    for stationId in stationIds:
        query_weather.s(stationId)
