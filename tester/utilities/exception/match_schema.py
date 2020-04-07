class AssertionException(Exception):
    def __init__(self, name, value, assertion_expression):
        super().__init__(
            '{name} = {value}, cannot pass the assertion {assertion_expression}'.format(
                name = name,
                value = value,
                assertion_expression = assertion_expression
            )
        )

class EnumerationException(Exception):
    def __init__(self, name, value, enumeration):
        super().__init__(
            '{name} = {value}, is not in the enumeration {enumeration}'.format(
                name = name,
                value = value,
                enumeration = enumeration
            )    
        )

class TypeMismatchException(Exception):
    def __init__(self, name, real_type, expected_types):
        super().__init__(
            'the type of {name} should be {expected_types}, but it was {real_type}'.format(
                name = name,
                real_type = real_type,
                expected_types = expected_types
            )
        )
