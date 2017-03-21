# -*- coding: utf-8 -*-
"""Manages virtual environments

Usage: vex [options] <virtual_environment_name> [<rest>]

Options:
       --always-copy         Use copies instead of creating symlinks
       --config PATH         Configuration file to read
       --cwd PATH            Path to run command in
    -l --list PREFIX         List virtual environment currently created
    -m --make                Make the virtual environment
       --path PATH           Open a specific path
    -p --python VERSION      Use a specific python version
    -r --remove              Remove the virtual environment
       --shell-config SHELL  Shell to use
       --site-packages       Allow system site package imports
    -V --version             Display version of vex
    -X --exit                Run a make/remove command and immediately exit
"""
from docopt import docopt


class Arg(object):
    """Converts docopt output into an argparser like object

    Args:
        docopt_options (dict): output from docopt
    """

    def __init__(self, docopt_options):
        def fix(key):
            key = key.lstrip('-')
            key = key.lstrip('<').rstrip('>')
            key = key.replace('-', '_')
            return key

        self._options = {
            fix(key): value
            for key, value in docopt_options.items()
        }

    def __getattr__(self, key):
        if not self.__hasattr__('_options'):
            value = super(Arg, self).__getattribute__(key)
        elif key not in self.__dict__['_options']:
            raise KeyError('Key not found: {key}'.format(key=key))
        else:
            if key in self.__dict__['_options']:
                value = self.__dict__['_options'][key]
            else:
                raise KeyError('Key not found: {key}'.format(key=key))
        return value

    def __hasattr__(self, key):
        try:
            super(Arg, self).__getattribute__('_options')
            attribute = True
        except AttributeError:
            attribute = False
        return attribute

    def __getitem__(self, key):
        return self._options[key]

    def __setattr__(self, key, value):
        if not self.__hasattr__('_options'):
            super(Arg, self).__setattr__(key, value)
        elif key not in self.__dict__['_options']:
            raise KeyError('Key not found: {key}'.format(key=key))
        else:
            if key in self.__dict__['_options']:
                self.__dict__['_options'][key] = value
            else:
                raise KeyError('Key not found: {key}'.format(key=key))

    def __setitem__(self, key, value):
        if key in self._options:
            self._options[key] = value
        else:
            raise KeyError('Key not found: {key}'.format(key=key))

    def __repr__(self):
        cname = self.__class__.__name__
        options = []
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            options.append((k, v))
        if options:
            options = ', '.join('{k}:{v}'.format(k=k, v=v) for k, v in options)
        else:
            options = ''
        string = '<{cname} {options}>'.format(cname=cname, options=options)
        return string


def make_arg_parser(argv, docstring=None):
    """Return a standard ArgumentParser object.
    """
    docstring = docstring or __doc__
    options = docopt(docstring, argv=argv)

    parser = Arg(docopt_options=options)
    return parser


def get_options(argv):
    """Called to parse the given list as command-line arguments.

    :returns:
        an options object as returned by argparse.
    """
    arg_parser = make_arg_parser(argv)
    return arg_parser
