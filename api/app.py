import logging

from flask import Flask, request, Response

from models.WeatherObservation import WeatherObservation
from models.WeatherStation import WeatherStation
from models.db import Database
from tasks.celery import hello

app = Flask(__name__)
logger = logging.getLogger(__name__)

# logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    hello.delay()
    return 'Hello World'

@app.route('/weather/<station_id>/<unit>', methods=['GET'])
def weather(station_id='KMAHANOV10', unit='imperial'):
    print(f'Station: {station_id}')
    # Moving the evaluation logic out of the resolver makes it easier to test and
    # makes the resolver more straightforward
    observationData = WeatherObservation.getOrCreateObservation(station_id)
    observationData = WeatherObservation.localize(observationData, unit)
    return observationData

@app.route('/observations/<station_id>', methods=['GET'])
def list_observations(station_id):
    db = Database()
    results = db.search('weather-observation', [{
        'key': 'stationId',
        'value': station_id
    }])
    return results


"""
Payload to include a new station for recording

{
    stationId: str
    stationName: str
}
"""
@app.route('/station/', methods=['POST'])
def addStation():
    requestBody = request.json
    stationId = requestBody['stationId']
    stationName = requestBody['stationName']
    station = WeatherStation(
        stationId=stationId,
        stationName=stationName
    )
    station.save()
    return station.serialize()




if __name__ == '__main__':
    app.run()
