import os
import inspect

from tester.utilities.argument_parser import ArgumentParser

from .meta_class import MetaClass
from .teststep_queue import TestStepQueue

class BaseTestCase(metaclass = MetaClass):
    """
    description: BaseTestCase 是测试用例的基类, 所有的测试用例都需要继承 BaseTestCase.
    """

    @classmethod
    def __initialize__(cls):
        pass

    @classmethod
    def __parse_argument__(cls):
        cls._base_name, _ = os.path.splitext(inspect.getfile(cls))

        argument_parser = ArgumentParser()

        argument_parser.add_argument(
            '-t', '--testsuite',
            action = 'store',
            type = str,
            default = None,
            help = 'specify the testsuite file path for this testcase'
        )

        argument_parser.add_argument(
            '-e', '--environment',
            action = 'store',
            type = str,
            default = cls.__document__.get(),
            help = 'specify the environment name for this testcase'
        )
