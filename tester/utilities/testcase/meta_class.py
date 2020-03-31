import os
import sys
import inspect
import yaml

from tester.utilities.constant import BASE_TESTCASE_NAME

from .is_teststep import is_teststep

class MetaClass(type):
    """
    description: 这个是测试用例基类 BaseTestCase 的元类.
    """

    def __prepare__(self, *args, **kwargs):
        return dict()

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.path.samefile(__file__, inspect.getfile(cls)):
            return

        main_file_path = sys.argv[0]

        if not os.path.isfile(main_file_path):
            return

        # if not has_teststep(cls):
        #     return

    def __new__(cls, name, bases, class_dict):
        base, *_ = (object,) if name == BASE_TESTCASE_NAME else bases

        for member in inspect.getmembers(base):
            if is_teststep(member = member):
                delattr(base, member.__name__)
        
        BaseTestCase = type.__new__(cls, name, bases, class_dict)

        if name == BASE_TESTCASE_NAME:
            return BaseTestCase

        BaseTestCase.__document__ == yaml.load(BaseTestCase.__doc__, Loader = yaml.SafeLoader)
        if not base.__name__ == BASE_TESTCASE_NAME:
            BaseTestCase.__document__ = {**base.__document__, **BaseTestCase.__document__}

        return BaseTestCase

    def __call__(cls, *args, **kwargs):
        TestCase = type.__call__(*args, **kwargs)

        file_path = inspect.getfile(cls)
        file_name, _ = os.path.splitext(os.path.basename(file_name))

        required_fields = [
            
        ]
