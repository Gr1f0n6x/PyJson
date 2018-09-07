import unittest
from pyjson.core import JsonMapper, to_json, from_json, _AvailableJsonMappers


class TestClass(object, metaclass=JsonMapper):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @classmethod
    def serialize(cls, o):
        return {'a': o.a, 'b': o.b}

    @classmethod
    def deserialize(cls, o):
        return TestClass(**o)

    def __eq__(self, other):
        if isinstance(other, TestClass):
            return self.a == other.a and self.b == other.b
        return False

    def __repr__(self):
        return 'TestClass: {0}, {1}'.format(self.a, self.b)


class Default(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        if isinstance(other, Default):
            return self.a == other.a and self.b == other.b
        return False

    def __repr__(self):
        return 'Default: {0}, {1}'.format(self.a, self.b)


class MappedWithNested(object, metaclass=JsonMapper):
    def __init__(self, a, b, nested):
        self.a = a
        self.b = b
        self.nested = nested

    @classmethod
    def serialize(cls, o):
        return {'a': o.a, 'b': o.b, 'nested': o.nested}

    @classmethod
    def deserialize(cls, o):
        return MappedWithNested(**o)

    def __eq__(self, other):
        if isinstance(other, MappedWithNested):
            return self.a == other.a and self.b == other.b and self.nested == other.nested
        return False

    def __repr__(self):
        return 'MappedWithNested: {0}, {1}, {2}'.format(self.a, self.b, self.nested)


class DefaultWithNested(object):
    def __init__(self, a, b, nested):
        self.a = a
        self.b = b
        self.nested = nested

    def __eq__(self, other):
        if isinstance(other, DefaultWithNested):
            return self.a == other.a and self.b == other.b and self.nested == other.nested
        return False


class JsonMapperTest(unittest.TestCase):
    def test_available_mappers(self):
        self.assertTrue('test.JsonMapperTest.TestClass' in _AvailableJsonMappers._mappers)

    def test_available_mappers_default(self):
        to_json(Default(1, 2))
        self.assertTrue('test.JsonMapperTest.Default' in _AvailableJsonMappers._mappers)

    def test_to_json(self):
        t = TestClass(1, 2)
        j = to_json(t)
        self.assertEqual("{\"a\": 1, \"b\": 2, \"__meta\": \"test.JsonMapperTest.TestClass\"}", j)

    def test_from_json(self):
        j = to_json(TestClass(1, 2))
        t = from_json(j)
        self.assertEqual(t, TestClass(1, 2))

    def test_to_json_default(self):
        t = Default(1, 2)
        j = to_json(t)
        self.assertEqual("{\"a\": 1, \"b\": 2, \"__meta\": \"test.JsonMapperTest.Default\"}", j)

    def test_from_json_default(self):
        j = "{\"a\": 1, \"b\": 2}"
        t = from_json(j)
        self.assertEqual(Default(**t), Default(1, 2))

    def test_nested_default_to_json(self):
        t = MappedWithNested(1, 2, Default(3, 4))
        j = to_json(t)
        self.assertEqual(
            "{\"a\": 1, \"b\": 2, \"nested\": {\"a\": 3, \"b\": 4, \"__meta\": \"test.JsonMapperTest.Default\"}, \"__meta\": \"test.JsonMapperTest.MappedWithNested\"}",
            j)

    def test_nested_mapped_to_json(self):
        t = MappedWithNested(1, 2, TestClass(3, 4))
        j = to_json(t)
        self.assertEqual(
            "{\"a\": 1, \"b\": 2, \"nested\": {\"a\": 3, \"b\": 4, \"__meta\": \"test.JsonMapperTest.TestClass\"}, \"__meta\": \"test.JsonMapperTest.MappedWithNested\"}",
            j)

    def test_nested_default_from_json(self):
        j = to_json(MappedWithNested(1, 2, Default(3, 4)))
        t = from_json(j)
        self.assertEqual(MappedWithNested(1, 2, Default(3, 4)), t)

    def test_nested_mapped_from_json(self):
        j = to_json(MappedWithNested(1, 2, TestClass(3, 4)))
        t = from_json(j)
        self.assertEqual(MappedWithNested(1, 2, TestClass(3, 4)), t)

    def test_default_nested_default_to_json(self):
        t = DefaultWithNested(1, 2, Default(3, 4))
        j = to_json(t)
        self.assertEqual(
            "{\"a\": 1, \"b\": 2, \"nested\": {\"a\": 3, \"b\": 4, \"__meta\": \"test.JsonMapperTest.Default\"}, \"__meta\": \"test.JsonMapperTest.DefaultWithNested\"}",
            j)

    def test_default_nested_default_from_json(self):
        j = to_json(DefaultWithNested(1, 2, Default(3, 4)))
        t = from_json(j)
        self.assertEqual(DefaultWithNested(1, 2, Default(3, 4)), t)

    def test_default_nested_mapped_to_json(self):
        t = DefaultWithNested(1, 2, TestClass(3, 4))
        j = to_json(t)
        self.assertEqual(
            "{\"a\": 1, \"b\": 2, \"nested\": {\"a\": 3, \"b\": 4, \"__meta\": \"test.JsonMapperTest.TestClass\"}, \"__meta\": \"test.JsonMapperTest.DefaultWithNested\"}",
            j)

    def test_default_nested_mapped_from_json(self):
        j = to_json(DefaultWithNested(1, 2, TestClass(3, 4)))
        t = from_json(j)
        self.assertEqual(DefaultWithNested(1, 2, TestClass(3, 4)), t)

    def test_default_collection_to_json(self):
        c = [Default(1, 2), Default(3, 4)]
        j = to_json(c)
        self.assertEqual('[{"a": 1, "b": 2, "__meta": "test.JsonMapperTest.Default"}, {"a": 3, "b": 4, "__meta": "test.JsonMapperTest.Default"}]', j)

    def test_default_collection_from_json(self):
        j = to_json([Default(1, 2), Default(3, 4)])
        c = from_json(j)
        self.assertEqual([Default(1, 2), Default(3, 4)], c)

    def test_mapped_collection_to_json(self):
        c = [TestClass(1, 2), TestClass(3, 4)]
        j = to_json(c)
        self.assertEqual('[{"a": 1, "b": 2, "__meta": "test.JsonMapperTest.TestClass"}, {"a": 3, "b": 4, "__meta": "test.JsonMapperTest.TestClass"}]', j)

    def test_mapped_collection_from_json(self):
        j = to_json([TestClass(1, 2), TestClass(3, 4)])
        c = from_json(j)
        self.assertEqual([TestClass(1, 2), TestClass(3, 4)], c)


if __name__ == '__main__':
    unittest.main()
