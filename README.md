# PyJson
Simple library for converting user defined classes to and from json 
## Usage

    from pyjson import JsonMapper
    
    class SomeClass(object, metaclass=JsonMapper):
        def __init__(self, a, b):
            self.a = a
            self.b = b
            
        @classmethod
        def serialize(cls, o):
            return {'a': o.a, 'b': o.b}
           
        @classmethod
        def deserialize(cls, o):
            return SomeClass(**o)
      

...     
    
    from pyjson import to_json, from_json
    from . import SomeClass
    
    if __name__ == '__main__':
        o = SomeClass(1, 2)
        json = to_json(o)  # '{"a": 1, "b": 2, "__meta": "SomeClass"}'
        ...
        b = from_json(json)
        