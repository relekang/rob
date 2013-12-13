import unittest
import redis

from rob.base import BaseObject
from rob.objects import JsonObject, HashObject

r = redis.Redis()
r.flushdb()


class BaseObjectTest(unittest.TestCase):
    TEST_DATA = {
        'title': 'Supertitle',
        'author': 'Some guy',
        'number': 2,
        'boolean': True
    }

    def test_init(self):
        item = BaseObject(**self.TEST_DATA)
        for key in self.TEST_DATA:
            self.assertEqual(getattr(item, key), self.TEST_DATA[key])


class ObjectTestCase(unittest.TestCase):

    BASE_DATA = {
        'key': 'a-key',
        'title': 'A fine title',
        'number': 10
    }

    def setUp(self):
        self.item = self.CLS.create(**self.BASE_DATA)

    def tearDown(self):
        self.item.delete()


class ObjectTestMixin(object):

    def assertObjectInStore(self, key, data_dict):
        item = self.CLS.get(key)
        self.assertEquals(len(item.__dict__.keys()), len(data_dict.keys()))
        for key in data_dict:
            self.assertEqual(getattr(item, key), data_dict[key])

    def test_save(self):
        self.item.title = 'Wat'
        self.item.save()
        self.assertEquals(self.CLS.get(self.item.key).title, 'Wat')
        self.assertEquals(self.CLS.count(), 1)

    def test_create(self):
        data = {
            'key': 'thing',
            'title': 'Awesome thing',
            'height': '20'
        }
        self.item2 = self.CLS.create(**data)
        self.assertEquals(self.CLS.count(), 2)
        self.assertObjectInStore('thing', data)
        self.item2.delete()

    def test_delete(self):
        self.item.delete()
        self.assertEquals(self.CLS.count(), 0)


class TestJsonObject(JsonObject):
    redis = r
    HASH_KEY = 'testjson'


class JsonObjectTest(ObjectTestCase, ObjectTestMixin):
    CLS = TestJsonObject


class TestHashObject(HashObject):
    redis = r
    HASH_KEY = 'testhash%s'


class HashObjectTest(ObjectTestCase, ObjectTestMixin):
    CLS = TestHashObject


if __name__ == '__main__':
    unittest.main()
