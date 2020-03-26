import os
import sys
import inspect

class MetaClass(type):
    """
    description: 这个是测试用例基类 BaseTestCase 的元类.
    """

    def __prepare__(self, *args, **kwargs):
        pass

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.path.samefile(__file__, inspect.getfile(cls)):
            return

        main_file_path = sys.argv[0]

        if not os.path.isfile(main_file_path):
            return

        if not has_teststep(cls):
            return
