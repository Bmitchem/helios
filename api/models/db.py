import redis
import json
from constants import REDIS_HOST, REDIS_PORT


class Database:
    redis_db = None
    def __init__(self):
        self.connect()

    def connect(self):
        self.redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)

    def save(self, pk, data):
        self.redis_db.set(pk, json.dumps(data))

    def fetch(self, pk):
        data = self.redis_db.get(pk)
        if data:
            return json.loads(data)
        return data

    def delete(self, pk):
        data = self.redis_db.delete(pk)
        return data is None