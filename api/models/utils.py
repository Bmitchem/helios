import datetime


def roundToNearestFiveMinutes(date: datetime.datetime) -> datetime:
    # in those instances where the minutes are already at target
    delta = date.minute % 5
    return datetime.datetime(
        date.year,
        date.month,
        date.day,
        date.hour,
        date.minute - delta,
        0, # Seconds
        0  # MS
    )

def convertFtoK(temp: int) -> float:
    kelvinTemp = (temp - 32) * (5 / 9) + 273.15
    return format(kelvinTemp, '.2f')
# (273.15K − 273.15) × 9/5 + 32 = 32°F
def convertKelvinToFahrenheit(kelvinTemp: float) -> str:
    fahrenheitTemp = (kelvinTemp - 273.15) * (9 / 5) + 32
    return format(fahrenheitTemp, '.2f')

# 373.15K − 273.15 = 100°C
def convertKelvinToCelsius(kelvinTemp: float) -> str:
    celsiusTemp = (kelvinTemp - 273.15)
    return format(celsiusTemp, '.2f')