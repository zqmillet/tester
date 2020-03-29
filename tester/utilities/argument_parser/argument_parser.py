import argparse
import textwrap
import colorama

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            formatter_class = argparse.RawTextHelpFormatter,
            ** kwargs
        )

    def add_argument(self, *args, **kwargs):
        if 'help' in kwargs:
            kwargs['help'] = kwargs['help'].strip().strip('.')
            comment_list = list()

            if 'type' in kwargs:
                comment_list.append(
                    '# parameter type: {type}'.format(
                        type = kwargs['type']
                    )
                )

            if 'default' in kwargs and not kwargs['default'] == argparse.SUPPRESS:
                comment_list.append(
                    '# default value: {default}'.format(
                        default = kwargs['default']
                    )
                )

            comment = '' if not comment_list else colorama.Fore.BLUE + \
                '\n' + '\n'.join(comment_list) + colorama.Fore.RESET

            kwargs['help'] = '\n'.join(
                sum([textwrap.wrap(line) for line in kwargs['help'].splitlines()], list())
            ) + comment

        super().add_argument(*args, **kwargs) 
