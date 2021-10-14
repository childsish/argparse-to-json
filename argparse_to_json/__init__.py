import argparse

from argparse_to_json.converter import Converter


def convert_parser_to_json(parser: argparse.ArgumentParser) -> dict:
    return Converter().convert(parser)
