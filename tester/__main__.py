import sys

from tester.utilities.argument_parser import ArgumentParser

from tester import version

class COMMANDS:
    CONFIG = 'config'
    TESTSUITE = 'testsuite'
    VERSION = 'version'
    MANUAL = 'manual'

def main():
    argument_parser = ArgumentParser()

    subparsers = argument_parser.add_subparsers(
        help = 'tester commands help',
        dest = 'command'
    )

    version_parser = subparsers.add_parser(
        COMMANDS.VERSION,
        help = 'get the version of tester'
    )

    testsuite_parser = subparsers.add_parser(
        COMMANDS.TESTSUITE,
        help = 'execute the testsuite'
    )

    arguments = argument_parser.parse_args(sys.argv[1:])

    if arguments.command == COMMANDS.VERSION:
        print(version)
    elif arguments.command == COMMANDS.TESTSUITE:
        execute_testsuite(arguments = arguments)

def execute_testsuite(arguments):
    pass

if __name__ == '__main__':
    main()
