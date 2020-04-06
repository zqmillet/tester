import ast
import inspect
import astunparse
import yaml

from tester.utilities.constant import SCHEMA_KEY
from tester.utilities.common import get_object_from_expression
from tester.utilities.exception import AssertionException
from tester.utilities.exception import EnumerationException

def __instantiate_assertion(schema):
    if not schema:
        return schema

    type_name = schema[SCHEMA_KEY.TYPE]

    if type_name == dict.__name__:
        for property_name in schema.get(SCHEMA_KEY.PROPERTIES, dict()):
            __instantiate_assertion(schema = schema[SCHEMA_KEY.PROPERTIES][property_name])

    elif type_name == list.__name__:
        if SCHEMA_KEY.ITEMS in schema:
            __instantiate_assertion(schema = schema[SCHEMA_KEY.ITEMS])

    if SCHEMA_KEY.ASSERTION in schema:
        assertion_expression = schema[SCHEMA_KEY.ASSERTION]
        schema[SCHEMA_KEY.ASSERTION_FUNCTION] = get_object_from_expression(assertion_expression)

def __instantiate_type(schema):
    if not schema:
        return schema

    type_name = schema[SCHEMA_KEY.TYPE]

    if type_name == dict.__name__:
        for property_name in schema.get(SCHEMA_KEY.PROPERTIES, dict()):
            __instantiate_type(schema = schema[SCHEMA_KEY.PROPERTIES][property_name])

    elif type_name == list.__name__:
        if SCHEMA_KEY.ITEMS in schema:
            __instantiate_type(schema = schema[SCHEMA_KEY.ITEMS])

    schema[SCHEMA_KEY.TYPE] = __get_types(schema)

def __get_name(name, parents):
    return name + ''.join(['[' + repr(item) + ']' for item in parents])

def __test_assertion(value, name, assertion, assertion_expression, parents):
    if assertion(value):
        return None

    return AssertionException(
        name = __get_name(name = name, parents = parents),
        value = repr(value),
        assertion_expression = assertion_expression 
    )

def __test_enumeration(value, name, enumeration, parents):
    if value in enumeration:
        return None

    return EnumerationException(
        name = __get_name(name = name, parents = parents),
        value = repr(value),
        enumeration = enumeration
    )
    
def __get_types(schema):
    types = schema[SCHEMA_KEY.TYPE]

    if not isinstance(types, list):
        types = [types]

    _types = list()
    for _type in types:
        if '.' in _type:
            package, name = _type.rsplit('.', 1)
            _types.append(
                get_object_from_expression(
                    'from {package} import {name}; {name}'.format(
                        name = name,
                        package = package
                    )
                )
            )
        elif _type == 'any':
            _types.append(object)
        else:
            _types.append(eval(_type))
    return tuple(_types)

def __match_schema(data, schema, parents, name):
    pass

def match_schema(data, schema, parents = None, name = 'variable'):
    if parents is None:
        parents = list()

    schema = yaml.load(schema, Loader = yaml.SafeLoader)

    __instantiate_assertion(schema)
    __instantiate_type(schema)
    import pdb; pdb.set_trace()
    return __match_schema(data = data, schema = schema, parents = parents, name = name)  

if __name__ == '__main__':
    schema = '''
    type: dict
    properties:
        name:
            type: str
        ags:
            type:
                - int
                - float
            assertion: "lambda x: 10 < x < 30"
    '''

    data = dict(
        name = 'qiqi',
        age = '2333'
    )

    exception = match_schema(data = data, schema = schema)
