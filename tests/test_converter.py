import argparse
import unittest

from argparse_to_json import convert_parser_to_json as convert


class TestConverter(unittest.TestCase):
    def test_empty_parser(self):
        parser = argparse.ArgumentParser()
        jsonform = convert(parser)
        self.assertEqual(jsonform, {
            'type': 'object',
            'properties': {},
            'required': [],
        })

    def test_positional_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input1')
        jsonform = convert(parser)
        self.assertEqual(jsonform, {
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'string',
                },
            },
            'required': ['input1'],
        })

    def test_optional_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input1')
        jsonform = convert(parser)
        self.assertEqual(jsonform, {
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'string',
                },
            },
            'required': [],
        })

    def test_optional_flag(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input1', action='store_true')
        jsonform = convert(parser)
        self.assertEqual(jsonform, {
            'type': 'object',
            'properties': {
                'input1': {
                    'type': 'boolean',
                },
            },
            'required': [],
        })
