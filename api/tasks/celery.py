import os
from celery import Celery

from models.db import Database

REDIS_HOST=os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT=os.environ.get("REDIS_PORT", "6379")

print(f'connecting to redis at: {REDIS_HOST}:{REDIS_PORT}')

app = Celery(
    'tasks',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # broker=f'{REDIS_HOST}:{REDIS_PORT}/0',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # backend=f'{REDIS_HOST}:{REDIS_PORT}/0',
    # include=['celery.tasks']
)

@app.task
def hello():
    with open('task_output.txt', 'w') as f:
        f.write('Hello World')

    return 'Hello World!'

@app.task
def save_observation(pk: str, observation: str):
    db = Database()
    db.save(pk, observation)
    return pk

@app.task
def save_station(pk: str, station: str):
    db = Database()
    db.save(pk, station)
    return pk