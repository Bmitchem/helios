import unittest

from pydantic_core import ValidationError

from models.WeatherObservation import WeatherObservation
from faker import Faker

def generateObservation():
    """
        example api output {
          "heatIndex": "35f",
          "humidity": 80,
          "obsTimeLocal": "2026-04-04 16:47:27",
          "stationID": "KMAHANOV10",
          "temp": "35f",
          "windChill": "30f"
        }

    :return:
    """
    fake = Faker()
    scale = fake.random_element(elements=['c','f'])
    return {
        "heatIndex":f"{fake.random_number(digits=2)}{scale}",
        "windChill":f"{fake.random_number(digits=2)}{scale}",
        "temp":f"{fake.random_number(digits=2)}{scale}",
        "humidity":f"{fake.random_number(digits=2)}",
        "obsTimeLocal":f"{fake.date('%Y-%m-%d %H:%M:%S')}",
        "stationId":f"{fake.uuid4()}",
    }

class WeatherObservationTests(unittest.TestCase):
    def test_farenheit_validation(self):
        testData = generateObservation()
        assert WeatherObservation(**testData)

    def test_heatIndex_int_throws_error(self):
        testData = generateObservation()
        testData['heatIndex'] = 0
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_windChill_int_throws_error(self):
        testData = generateObservation()
        testData['windChill'] = 0
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_temp_int_throws_error(self):
        testData = generateObservation()
        testData['temp'] = 0
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_humidity_str_throws_error(self):
        testData = generateObservation()
        testData['humidity'] = 'foo'
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)


if __name__ == '__main__':
    unittest.main()
