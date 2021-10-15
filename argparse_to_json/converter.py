import argparse


class Converter:
    def convert(self, parser: argparse.ArgumentParser, properties=None, required=None) -> dict:
        properties = {} if properties is None else properties
        required = [] if required is None else required
        for action in parser._actions[1:]:
            self.parse_action(action, properties, required)
        return {
            'type': 'object',
            'properties': properties,
            'required': required,
        }

    def parse_action(self, action, properties, required):
        action_name = type(action).__name__
        self.parse_store_action(action, properties, required) if action_name == '_StoreAction' else\
            self.parse_store_true_action(action, properties, required) if action_name == '_StoreTrueAction' else\
            self.parse_subparsers_action(action, properties, required) if action_name == '_SubParsersAction' else\
            None
        if action.required:
            required.append(action.dest)

    def parse_store_action(self, action, properties, required):
        properties[action.dest] = {
            'type': 'string'
        }
        if action.help:
            properties[action.dest]['description'] = action.help
        if action.choices:
            properties[action.dest]['enum'] = action.choices

    def parse_store_true_action(self, action, properties, required):
        properties[action.dest] = {
            'type': 'boolean',
        }
        if action.help:
            properties[action.dest]['description'] = action.help

    def parse_subparsers_action(self, action, properties, required):
        properties[action.container.title] = {
            'type': 'string',
            'enum': list(action.choices),
        }
        if action.help:
            properties['subform_selector']['description'] = action.help
        for name, parser in action.choices.items():
            properties[name] = self.convert(parser)
        required.append(action.container.title)
