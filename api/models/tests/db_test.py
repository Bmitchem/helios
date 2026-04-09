import unittest
from unittest.mock import MagicMock

from api.models.db import Database
from WeatherStation_test import generateStation

class TestDatabase(unittest.TestCase):
    def test_save_Fetch(self):
        data = {
            'id': 1,
            'value': 'foo'
        }

        db = Database()
        db.save(data['id'], data)
        returned_doc = db.fetch(data['id'])
        assert returned_doc is not None
        assert returned_doc['value'] == data['value']

    def test_save_Fetch_primitive(self):
        db = Database()
        db.save(1, 'foo')
        returned_doc = db.fetch(1)
        assert returned_doc is not None
        assert returned_doc == 'foo'

    def test_save_delete(self):
        db = Database()
        db.save(1, 'foo')
        returned_doc = db.fetch(1)
        assert returned_doc is not None
        assert returned_doc == 'foo'

        db.delete(1)
        returned_doc = db.fetch(1)
        assert returned_doc is None

    def test_save_key_conflict(self):
        db = Database()
        db.save(1, 'foo')
        db.save(1, 'bar')
        returned_doc = db.fetch(1)
        assert returned_doc is not None
        assert returned_doc == 'bar'


    def test_search(self):
        keys = [f'prefix-{x}' for x in range(10)]
        db = Database()
        db.redis_db.scan_iter = MagicMock(return_value=keys)
        db.fetch = MagicMock(side_effect=lambda x : generateStation())

        results = db.search('prefix', [])
        assert len(results) == len(keys)



if __name__ == '__main__':
    unittest.main()
