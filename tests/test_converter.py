import argparse
import unittest

from argparse_to_json import convert_parser_to_json as convert


class TestConverter(unittest.TestCase):
    def test_empty_parser(self):
        parser = argparse.ArgumentParser()
        jsonform = convert(parser)
        self.assertEqual({
            'type': 'object',
            'properties': {},
            'required': [],
        }, jsonform)

    def test_positional_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input1')
        jsonform = convert(parser)
        self.assertEqual({
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'string',
                },
            },
            'required': ['input1'],
        }, jsonform)

    def test_positional_argument_with_choices(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input1', choices=['foo', 'bar'])
        jsonform = convert(parser)
        self.assertEqual({
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'string',
                    'enum': ['foo', 'bar'],
                },
            },
            'required': ['input1'],
        }, jsonform)

    def test_optional_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input1')
        jsonform = convert(parser)
        self.assertEqual({
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'string',
                },
            },
            'required': [],
        }, jsonform)

    def test_optional_flag(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input1', action='store_true')
        jsonform = convert(parser)
        self.assertEqual({
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'boolean',
                },
            },
            'required': [],
        }, jsonform)

    def test_subparsers(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        subparser1 = subparsers.add_parser('subparser1')
        subparser2 = subparsers.add_parser('subparser2')
        jsonform = convert(parser)
        self.assertEqual({
            'type': 'object',
            'properties': {
                'positional arguments': {
                    'type': 'string',
                    'enum': ['subparser1', 'subparser2'],
                },
                'subparser1': {
                    'type': 'object',
                    'properties': {},
                    'required': [],
                },
                'subparser2': {
                    'type': 'object',
                    'properties': {},
                    'required': [],
                },
            },
            'required': ['positional arguments'],
        }, jsonform)
