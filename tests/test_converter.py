import argparse
import unittest

from argparse_to_json import convert_parser_to_json as convert


class TestConverter(unittest.TestCase):
    def test_empty_parser(self):
        parser = argparse.ArgumentParser()
        jsonform = convert(parser)
        self.assertEqual({
            'schema': {}
        }, jsonform)

    def test_positional_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input1')
        jsonform = convert(parser)
        self.assertEqual({
            'schema': {
                'input1': {
                    'type': 'string',
                    'required': True,
                },
            },
        }, jsonform)

    def test_positional_argument_with_choices(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input1', choices=['foo', 'bar'])
        jsonform = convert(parser)
        self.assertEqual({
            'schema': {
                'input1': {
                    'type': 'string',
                    'enum': ['foo', 'bar'],
                    'required': True,
                },
            },
        }, jsonform)

    def test_optional_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input1')
        jsonform = convert(parser)
        self.assertEqual({
            'schema': {
                'input1': {
                    'type': 'string',
                },
            },
        }, jsonform)

    def test_optional_flag(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input1', action='store_true')
        jsonform = convert(parser)
        self.assertEqual({
            'schema': {
                'input1': {
                    'type': 'boolean',
                },
            },
        }, jsonform)

    def test_subparsers(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        subparsers.add_parser('subparser1')
        subparsers.add_parser('subparser2')
        jsonform = convert(parser)
        self.assertEqual({
            'schema': {
                'subparser1': {
                    'type': 'object',
                    'properties': {},
                },
                'subparser2': {
                    'type': 'object',
                    'properties': {},
                },
            },
            'form': [
                {
                    'type': 'selectFieldSet',
                    'title': 'Choose command',
                    'items': [
                        {
                            'key': 'subparser1',
                        },
                        {
                            'key': 'subparser2',
                        }
                    ],
                },
            ],
        }, jsonform)
