import json

from robjects.base import BaseObject


class JsonObject(BaseObject):

    def save(self):
        return self.redis.hset(
            self.HASH_KEY,
            self.key,
            json.dumps(self.__dict__)
        )

    def delete(self):
        return self.redis.hdel(self.HASH_KEY, self.key)

    @classmethod
    def all(cls):
        data = cls.redis.hgetall(cls.HASH_KEY)
        return [cls(**json.loads(data[key])) for key in data]

    @classmethod
    def count(cls):
        return len(cls.redis.hgetall(cls.HASH_KEY))

    @classmethod
    def get(cls, key):
        return cls(**json.loads(cls.redis.hget(cls.HASH_KEY, key)))
