# rob

[![Build Status](https://travis-ci.org/relekang/rob.png?branch=master)](https://travis-ci.org/relekang/rob)

Persistent python objects with Redis backend.

    pip install rob

### JsonObject
An object that does a JSON dump of the dictionary
and save it in a Redis hash.

Needs to define `HASH_KEY` - the key to the hash.
 
### HashObject
An object that saves its dictionary in a Redis hash. Using the HMSET.
It uses a list to keep track of saved objects.

Needs to define `HASH_KEY` - a key that is used as prefix to the list and
as the key to the hash.

### Mixins
The mixins below will work with all the object types.

#### Autosave mixin
A mixin that calls save every time an attribute is set.

## Examples

#### Simple object
```python
from redis import Redis


class ExampleObject(JsonObject):
    HASH_KEY = 'exampleobject'
    redis = Redis()
```

#### Autosave object
```python
from redis import Redis


class ExampleAutosaveObject(JsonObject, AutosaveMixin):
    HASH_KEY = 'exampleobject'
    redis = Redis()
```
