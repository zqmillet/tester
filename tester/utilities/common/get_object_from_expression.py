import ast
import types
import astunparse

def get_object_from_expression(expression, name = '__last_object__'):
    tree = ast.parse(expression)
    last_value = tree.body.pop().value

    previous_expression = astunparse.unparse(tree)
    last_expression = '='.join([name, astunparse.unparse(last_value).strip()])

    module = types.ModuleType(name = name)
    for expression in [previous_expression, last_expression]:
        exec(expression, module.__dict__)

    return module.__dict__[name]
