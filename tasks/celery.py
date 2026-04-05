from celery import Celery
import os

REDIS_HOST=os.environ.get("REIDS_HOST", "localhost")
REDIS_PORT=os.environ.get("REIDS_PORT", "6379")

print(f'connecting to redis at: {REDIS_HOST}:{REDIS_PORT}')

app = Celery(
    'tasks',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    # include=['celery.tasks']
)

@app.task
def hello():
    with open('task_output.txt', 'w') as f:
        f.write('Hello World')

    return 'Hello World!'