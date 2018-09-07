import json
from json import JSONDecoder, JSONEncoder


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


def _is_primitive(obj):
    return not hasattr(obj, '__dict__')


def _full_name(clazz):
    m = clazz.__class__.__module__
    if m:
        return '{0}.{1}'.format(m, clazz.__class__.__name__)
    return clazz.__class__.__name__


class _Encoder(JSONEncoder, metaclass=_Singleton):
    def default(self, o):
        if _AvailableJsonMappers.exist(_full_name(o)):
            encoder = _AvailableJsonMappers.encoder(_full_name(o))
            encoded = encoder(o)
            encoded.update({'__meta': _full_name(o)})
            return encoded
        elif not _is_primitive(o):
            _AvailableJsonMappers.add_new_mapper(name=_full_name(o), encoder=lambda e: e.__dict__, decoder=lambda d: o.__class__(**d))
            encoded = o.__dict__
            encoded.update({'__meta': _full_name(o)})
            return encoded
        else:
            return super().default(o)


class _Decoder(JSONDecoder, metaclass=_Singleton):
    def __init__(self):
        JSONDecoder.__init__(self, object_hook=self.object_hook)

    def object_hook(self, o):
        if _AvailableJsonMappers.exist(o.get('__meta', None)):
            decoder = _AvailableJsonMappers.decoder(o.get('__meta'))
            return decoder({k: v for k, v in o.items() if k != '__meta'})
        return o


class _AvailableJsonMappers(object, metaclass=_Singleton):
    _mappers = {}

    @classmethod
    def add_new_mapper(cls, name, encoder, decoder):
        if name not in cls._mappers:
            cls._mappers[name] = {'to': encoder, 'from': decoder}

    @classmethod
    def encoder(cls, name):
        if name in cls._mappers:
            return cls._mappers[name]['to']
        return None

    @classmethod
    def decoder(cls, name):
        if name in cls._mappers:
            return cls._mappers[name]['from']
        return None

    @classmethod
    def exist(cls, name):
        return name in cls._mappers


class JsonMapper(type):
    def __new__(mcs, *args, **kwargs):
        clazz = super(JsonMapper, mcs).__new__(mcs, *args, **kwargs)

        if not hasattr(clazz, 'serialize') or not hasattr(clazz, 'deserialize'):
            raise RuntimeError('Class should implement both static methods: serialize and deserialize')

        serialize = getattr(clazz, 'serialize')
        deserialize = getattr(clazz, 'deserialize')

        m = clazz.__module__
        if m:
            full_name = '{0}.{1}'.format(m, clazz.__name__)
        else:
            full_name = clazz.__name__

        _AvailableJsonMappers.add_new_mapper(name=full_name, encoder=serialize, decoder=deserialize)
        return clazz


def to_json(o):
    return json.dumps(o, cls=_Encoder)


def from_json(o):
    return json.loads(o, cls=_Decoder)
