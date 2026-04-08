import unittest

from pydantic_core import ValidationError

from faker import Faker

from models.WeatherObservation import WeatherObservation


def generateObservation():
    """
        example api output {
          "heatIndex": 35,
          "humidity": 80,
          "obsTimeLocal": "2026-04-04 16:47:27",
          "stationID": "KMAHANOV10",
          "temp": 35,
          "windChill": 30
        }

    :return:
    """
    fake = Faker()
    return {
        "heatIndex":fake.random_number(digits=2),
        "windChill":fake.random_number(digits=2),
        "temp":fake.random_number(digits=2),
        "humidity":fake.random_number(digits=2),
        "obsTimeLocal":f"{fake.date('%Y-%m-%d %H:%M:%S')}",
        "stationId":f"{fake.uuid4()}",
    }

class WeatherObservationTests(unittest.TestCase):
    def test_farenheit_validation(self):
        testData = generateObservation()
        assert WeatherObservation(**testData)

    def test_heatIndex_str_throws_error(self):
        testData = generateObservation()
        testData['heatIndex'] = "0f"
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_windChill_str_throws_error(self):
        testData = generateObservation()
        testData['windChill'] = "0f"
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_temp_str_throws_error(self):
        testData = generateObservation()
        testData['temp'] = "0f"
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_humidity_str_throws_error(self):
        testData = generateObservation()
        testData['humidity'] = 'foo'
        with self.assertRaises(ValidationError):
            WeatherObservation(**testData)

    def test_serialize(self):
        testData = generateObservation()
        observation = WeatherObservation(**testData)
        serialized_data = observation.serialize()
        assert isinstance(serialized_data, dict)

    def test_pk(self):
        testData = generateObservation()
        observation = WeatherObservation(**testData)
        assert isinstance(observation.pk, str)

if __name__ == '__main__':
    unittest.main()
