import os

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_HOST = os.environ.get('REDIS_URL', '0.0.0.0')