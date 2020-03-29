from .meta_class import MetaClass

class BaseTestCase(metaclass = MetaClass):
    """
    description: BaseTestCase 是测试用例的基类, 所有的测试用例都需要继承 BaseTestCase.
    """

    @classmethod
    def __initialize__(cls):
        pass
