# coding: utf-8

import sys, os
import argparse

import logging, coloredlogs

from .error import Error

def file_argument(string):
    """ Helper for argparse
        to verify the given argument is an existing file
    """
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError(
                "{0!r} is not an existing file".format(string)
            )
    return string

def dir_argument(string):
    """ Helper for argparse
        to verify the given argument is an existing directory
    """
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError(
                "{0!r} is not an existing directory".format(string)
            )
    return string

class ArgumentParser(argparse.ArgumentParser):

    def print_help(self):
        import humanfriendly.terminal
        humanfriendly.terminal.usage(self.format_help())

class Script():

    def __init__(self, script_name,
        description=None,
        description_epilog=None,
        config=None
    ):
        self.config = config

        # setup argument parser
        self.parser = ArgumentParser(
            description=description, epilog=description_epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        self.parser.add_argument('-v', '--verbose', action='store_const',
            dest='loglevel', const=logging.INFO, default=logging.WARN,
            help='enable log messages')
        self.parser.add_argument('-d', '--debug', action='store_const',
            dest='loglevel', const=logging.DEBUG, default=logging.WARN,
            help='enable debug messages')
        self.parser.add_argument('-q', '--quiet', action='store_true',
            help='do not print status messages')

        if self.config is not None:
            self.parser.add_argument('-c', '--config', action='store', required=True,
                help='configuration file')

        # setup environment
        if 'SCRIPT' not in os.environ or not os.getenv('SCRIPT'):
            os.environ['SCRIPT'] = script_name

    def run(self, main, args=None):
        # parse arguments
        self.arguments = self.parser.parse_args() if args == None else self.parser.parse_args(args)

        # setup logging
        formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
        stream = logging.StreamHandler()
        stream.setLevel(self.arguments.loglevel)
        stream.setFormatter(formatter)
        logging.root.setLevel(self.arguments.loglevel)
        logging.root.addHandler(stream)

        # parse configuration
        if self.config is not None:
            self.config.parse(self.arguments.config)

        # execute script
        try:
            main(self.arguments, self.config)

            sys.exit(0)

        # catch errors and exit
        except Error as e:
            logging.error(e.message)
            sys.exit(1)
