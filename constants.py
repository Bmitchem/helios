import os

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_URL = os.environ.get('REDIS_URL', '0.0.0.0')