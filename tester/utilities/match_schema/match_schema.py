import ast
import inspect
import astunparse
import yaml

from tester.utilities.constant import SCHEMA_KEY

def instantiate_assertion(schema):
    if not schema:
        return schema

    type_name = schema[SCHEMA_KEY.TYPE]

    if type_name == dict.__name__:
        for property_name in schema.get(SCHEMA_KEY.PROPERTIES, dict()):
            schema[SCHEMA_KEY.PROPERTIES][property_name] = instantiate_assertion(
                schema = schema[SCHEMA_KEY.PROPERTIES][property_name]
            )
    elif type_name == list.__name__:
        if SCHEMA_KEY.ITEMS in schema:
            schema[SCHEMA_KEY.ITEMS] = instantiate_assertion(
                schema = schema[SCHEMA_KEY.ITEMS]
            )

    if SCHEMA_KEY.ASSERTION in schema:
        assertion_expression = schema[SCHEMA_KEY.ASSERTION]
        schema[SCHEMA_KEY.ASSERTION] = get_
