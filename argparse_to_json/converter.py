import argparse


class Converter:
    def convert(self, parser: argparse.ArgumentParser) -> dict:
        properties = {}
        required = []
        for action in parser._actions[1:]:
            properties[action.dest] = self.parse_action(action)
            if action.required:
                required.append(action.dest)
        return {
            'type': 'object',
            'properties': properties,
            'required': required,
        }

    def parse_action(self, action):
        action_name = type(action).__name__
        data = self.parse_store_action(action) if action_name == '_StoreAction' else\
            self.parse_store_true_action(action) if action_name == '_StoreTrueAction' else\
            None
        if action.help:
            data['description'] = action.help
        return data

    def parse_store_action(self, action):
        data = {
            'type': 'string'
        }
        if action.choices:
            data['enum'] = action.choices
        return data

    def parse_store_true_action(self, action):
        return {
            'type': 'boolean',
        }
