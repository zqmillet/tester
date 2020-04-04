import sys
import inspect
import ast
import astunparse

def get_name(value):
    frame = sys._getframe().f_back
    tree = ast.parse(inspect.getsource(frame.f_back))

    for element in tree.body:
        if element.lineno == frame.f_back.f_lineno:
            if element.value.keywords:
                print(astunparse.unparse(element.value.keywords[0].value).strip() + ' = ' + repr(value))
            else:
                print(astunparse.unparse(element.value.args[0]).strip() + ' = ' + repr(value))

a = 3
b = []

def assert_that(value):
    get_name(value)

assert_that(value = a)
assert_that(b)
assert_that(value = list())
