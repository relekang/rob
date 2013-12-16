import json

from rob.base import BaseObject


class JsonObject(BaseObject):
    """
    An object that does a JSON dump of the dictionary
    and save it in a Redis hash.

    Needs to define `HASH_KEY` - the key to the hash.
    """

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


class HashObject(BaseObject):
    """
    An object that saves its dictionary in a Redis hash. Using the HMSET.
    It uses a list to keep track of saved objects.

    Needs to define `HASH_KEY` - a key that is used as prefix to the list and
    as the key to the hash.
    """

    def save(self):
        if not self.key in self.redis.lrange(self.list_key(), 0, -1):
            self.redis.lpush(self.list_key(), self.key)
        return self.redis.hmset(self.HASH_KEY % self.key, self.__dict__)

    def delete(self):
        hash_key = self.HASH_KEY % self.key
        self.redis.lrem(self.list_key(), self.key, 1)
        for key in self.redis.hkeys(hash_key):
            self.redis.hdel(hash_key, key)

    @classmethod
    def list_key(cls):
        return cls.HASH_KEY % 'keylist'

    @classmethod
    def all(cls):
        keys = cls.redis.lrange(cls.list_key(), 0, -1)
        return [cls(**cls.get(key)) for key in keys]

    @classmethod
    def count(cls):
        return len(cls.redis.lrange(cls.list_key(), 0, -1))

    @classmethod
    def get(cls, key):
        return cls(**cls.redis.hgetall(cls.HASH_KEY % key))
