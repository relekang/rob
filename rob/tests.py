import unittest
import redis

from rob.base import BaseObject
from rob.objects import JsonObject, HashObject
from rob.mixins import AutosaveMixin

r = redis.Redis(db='10')
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
    """
    A setup and tear down base for persistent objects.
    """

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
    """
    A mixin with tests that all types of persistent object should pass.
    """

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


class TestAutosaveObject(TestJsonObject, AutosaveMixin):
    pass


class AutosaveTest(ObjectTestCase, ObjectTestMixin):
    CLS = TestAutosaveObject

    def test_autosave(self):
        new_title = 'autosaved object'
        self.item.title = new_title
        self.assertEqual(TestAutosaveObject.get('a-key').title, new_title)


if __name__ == '__main__':
    unittest.main()
