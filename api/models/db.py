import redis
import json

from pydantic import BaseModel

from constants import REDIS_HOST, REDIS_PORT

class SearchParam(BaseModel):
    key: str
    value: str


class Database:
    redis_db = None
    dbName = None
    def __init__(self, dbName = 1):
        self.connect()
        self.dbName = dbName

    def connect(self):
        self.redis_db = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=self.dbName,
            decode_responses=True
        )

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

    def search(self, prefix:str, searchQuery: list[SearchParam]):
        matchedItems = []

        for dbKey in filter(lambda item: prefix in item, self.redis_db.scan_iter()):
            databaseObject = self.fetch(dbKey)
            matched = True
            for query in searchQuery:
                keyword = query['key']
                keyValue = query['value']
                if databaseObject.get(keyword) != keyValue:
                    matched = False
            if matched:
                matchedItems.append(databaseObject)
        return matchedItems
