import unittest

from api.models.db import Database

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



if __name__ == '__main__':
    unittest.main()
