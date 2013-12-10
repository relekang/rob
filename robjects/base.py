class BaseObject(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        item = cls(**kwargs)
        item.save()
        return item

    @classmethod
    def count(cls):
        return len(cls.all())

    @classmethod
    def all(cls):
        raise NotImplementedError

    @classmethod
    def get(cls, key):
        raise NotImplementedError
