from models.db import Database


class DatabaseModel:
    def save(self):
        database = Database()
        serialized_data = self.serialize()
        database.save(self.pk, serialized_data)
        return self

    def update(self, data=None):
        if data is None:
            response_data = self.fetch(self.pk)
            self._data = response_data
        else:
            self.save()
        return self

    def serialize(self) -> str:
        raise NotImplementedError



