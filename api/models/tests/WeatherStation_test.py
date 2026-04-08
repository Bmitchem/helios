import unittest

from faker import Faker

from models.WeatherStation import WeatherStation


def generateStation():
    """
        example api output {
          "stationName": "James Kirk Station",
          "stationId": "KMAHANOV10",
        }

    :return:
    """
    fake = Faker()
    scale = fake.random_element(elements=['c','f'])
    return {
        "stationName":fake.name(),
        "stationId":f"{fake.uuid4()}",
    }

class WeatherStationTests(unittest.TestCase):
    def test_stationId_validation(self):
        testData = generateStation()
        assert WeatherStation(**testData)

    def test_stationName_validation(self):
        testData = generateStation()
        assert WeatherStation(**testData)

if __name__ == '__main__':
    unittest.main()
