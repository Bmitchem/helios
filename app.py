import requests
from flask import Flask

from constants import WEATHER_API_KEY

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/weather/<station_id>', methods=['GET'])
def weather(station_id='KMAHANOV10'):
    print(f'Station: {station_id}')

    REQUEST_URL = f'https://api.weather.com/v2/pws/observations/current?stationId={station_id}&format=json&units=e&apiKey={WEATHER_API_KEY}'
    response = requests.get(REQUEST_URL)
    if response.ok:
        payload = response.json()
        observation = payload['observations'][0]
        return {
            'heatIndex': f"{observation['imperial']['heatIndex']}f",
            'windChill': f"{observation['imperial']['windChill']}f",
            'temp': f"{observation['imperial']['temp']}f",
            'humidity': observation['humidity'],
            "obsTimeLocal": observation['obsTimeLocal'],
            "stationID": observation['stationID']
        }
    else:
        print(response.content)


if __name__ == '__main__':
    app.run()
