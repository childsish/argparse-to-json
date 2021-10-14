import argparse


class Converter:
    def convert(self, parser: argparse.ArgumentParser) -> dict:
        properties = {}
        required = []
        for action in parser._actions[1:]:
            properties[action.dest] = {
                'type': 'boolean' if action.const is True and action.default is False else 'string'
            }
            if action.help:
                properties[action.dest]['description'] = action.help
            if action.required:
                required.append(action.dest)
        return {
            'type': 'object',
            'properties': properties,
            'required': required,
        }
