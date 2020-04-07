import ast
import inspect
import astunparse
import yaml

from tester.utilities.constant import SCHEMA_KEY
from tester.utilities.common import get_object_from_expression
from tester.utilities.exception import AssertionException
from tester.utilities.exception import EnumerationException
from tester.utilities.exception import TypeMismatchException

def __instantiate_assertion(schema):
    '''
    description: 这个函数用来实例化 schema 中的 assertion 字段. 该函数会对 schema 数据进行递归遍历.
    arguments:
        schema:
            type: dict
            description: 数据定义 schema.
            properties:
                type:
                    type: str
                    description: 数据的类型.
                    required: true
                properties:
                    type: dict
                    description: 如果数据类型是字典, 则该字段是字段的描述.
                    required: false
                items:
                    type: dict
                    description: 如果数据类型是列表, 则该字段是元素的描述.
                    required: false
                assertion:
                    type: str
                    description: 数据类型的断言表达式.
                    required: false
    return:
        type: type(None)
        description: 本函数无返回值, 而是直接修改 schema 的内容.
    '''

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
    '''
    description: 这个函数用来实例化 schema 中的 type 字段. 该函数会对 schema 数据进行递归遍历.
    arguments:
        schema:
            type: dict
            description: 数据定义 schema.
            properties:
                type:
                    type: str
                    description: 数据的类型.
                    required: true
                properties:
                    type: dict
                    description: 如果数据类型是字典, 则该字段是字段的描述.
                    required: false
                items:
                    type: dict
                    description: 如果数据类型是列表, 则该字段是元素的描述.
                    required: false
    return:
        type: type(None)
        description: 本函数无返回值, 而是直接修改 schema 的内容.
    '''

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

def __test_assertion(data, name, assertion, assertion_expression, parents):
    if assertion is None or assertion(data):
        return None

    return AssertionException(
        name = __get_name(name = name, parents = parents),
        data = repr(data),
        assertion_expression = assertion_expression 
    )

def __test_enumeration(data, name, enumeration, parents):
    if enumeration is None or data in enumeration:
        return None

    return EnumerationException(
        name = __get_name(name = name, parents = parents),
        data = repr(data),
        enumeration = enumeration
    )
    
def __get_types(schema):
    '''
    description: 这个函数是用来将 schema 的 type 字段, 由 str 类型实例化成 tuple 类型. 便于以后的运算.
    arguments:
        schema:
            type: dict
            description: 数据定义 schema.
            properties:
                type:
                    type:
                        - str
                        - list
                    description: 数据定义 schema 的 type 字段, 本身是一段 python 代码.
                    required: true
                    items:
                        type: str
                    examples:
                        - str
                        - int
                        - type(None)
                        - any
                        - testet.utilities.argumet_parser:ArgumentParser
                        - - int
                          - float
    return:
        type: tuple
        description: 返回数据类型构成的一个元组.
        items:
            type: type
    author: qiqi
    '''
    types = schema[SCHEMA_KEY.TYPE]

    if not isinstance(types, list):
        types = [types]

    _types = list()
    for _type in types:
        if ':' in _type:
            package, name = _type.rsplit(':', 1)
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
    expected_types = schema[SCHEMA_KEY.TYPE]

    if not isinstance(data, expected_types):
        return TypeMismatchException(
            name = name,
            real_type = type(data),
            expected_types = expected_types
        )

    exception = __test_enumeration(
        name = name,
        parents = parents,
        enumeration = schema.get(SCHEMA_KEY.ENUMERATION, None),
        data = data
    )
    if exception: return exception

    exception = __test_assertion(
        data = data,
        name = name,
        assertion = schema.get(SCHEMA_KEY.ASSERTION_FUNCTION, None),
        assertion_expression = schema.get(SCHEMA_KEY.ASSERTION, None),
        parents = parents
    )
    if exception: return exception

    if isinstance(data, dict):
        if SCHEMA_KEY.PROPERTIES not in schema:
            return None

        for property_name, property_schema in schema[SCHEMA_KEY.PROPERTIES].items():
            if property_schema.get(SCHEMA_KEY.REQUIRED, True) and property_name not in data:
                return Miss

def match_schema(data, schema, name = 'variable'):
    schema = yaml.load(schema, Loader = yaml.SafeLoader)

    __instantiate_assertion(schema)
    __instantiate_type(schema)
    return __match_schema(data = data, schema = schema, parents = list(), name = name)  

if __name__ == '__main__':
    schema = '''
    type:
        - dict
        - list
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
    print(exception)
