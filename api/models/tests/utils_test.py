import datetime
import unittest
from api.models.utils import roundToNearestFiveMinutes, convertFtoK, convertKelvinToFahrenheit
from models.utils import convertKelvinToCelsius


class TestRounding(unittest.TestCase):
    def test_round_no_rounding_0(self):
        dt = datetime.datetime(2026, 4, 6, 3, 20, 58)
        rounded = roundToNearestFiveMinutes(dt)
        self.assertEqual(rounded.minute, 20)
        self.assertEqual(rounded.second, 0)

    def test_round_no_rounding_5(self):
        dt = datetime.datetime(2026, 4, 6, 3, 35, 58)
        rounded = roundToNearestFiveMinutes(dt)
        self.assertEqual(rounded.minute, 35)
        self.assertEqual(rounded.second, 0)

    def test_round_down(self):
        dt = datetime.datetime(2026, 4, 6, 3, 13, 58)
        rounded = roundToNearestFiveMinutes(dt)
        self.assertEqual(rounded.minute, 10)

# fahrenheit
class TestFahrenheitConversion(unittest.TestCase):
    def test_freezing_Fahrenheit_conversion(self):
        kelvin = convertFtoK(32)
        assert kelvin == 273.15

    def test_boiling_Fahrenheit_conversion(self):
        kelvin = convertFtoK(212)
        assert kelvin == 373.15

    def test_freezing_kelvin_to_fahrenheit_conversion(self):
        fahrenheit = convertKelvinToFahrenheit(273.15)
        assert fahrenheit == "32f", f"expected {fahrenheit} to be 32f"

    def test__boiling_kelvin_to_fahrenheit_conversion(self):
        fahrenheit = convertKelvinToFahrenheit(373.15)
        assert fahrenheit == "212f", f"expected {fahrenheit} to be 212f"

    def test_freezing_kelvin_to_celsius_conversion(self):
        celsius = convertKelvinToCelsius(273.15)
        assert celsius == "0c", f"expected {celsius} to be 0c"

    def test__boiling_kelvin_to_celsius_conversion(self):
        celsius = convertKelvinToCelsius(373.15)
        assert celsius == "100c", f"expected {celsius} to be 100c"

if __name__ == '__main__':
    unittest.main()
