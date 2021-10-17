import argparse

from typing import Optional


class Converter:
    def convert(
        self,
        parser: argparse.ArgumentParser,
        schema: Optional[dict] = None,
        form: Optional[list] = None
    ) -> dict:
        schema = {} if schema is None else schema
        form = [] if form is None else form
        self.parse_parser(parser, schema, form)
        object = {
            'schema': schema,
        }
        if len(form) > 0:
            object['form'] = form
        return object

    def parse_parser(self, parser: argparse.ArgumentParser, schema: Optional[dict] = None, form: Optional[list] = None):
        schema = {} if schema is None else schema
        form = [] if form is None else form
        for action in parser._actions[1:]:
            self.parse_action(action, schema, form)
        return schema, form

    def parse_action(self, action: argparse.Action, schema: dict, form: list):
        action_name = type(action).__name__
        fn = {
            '_StoreAction': self.parse_store_action,
            '_StoreConstAction': self.parse_store_const_action,
            '_StoreTrueAction': self.parse_store_const_action,
            '_StoreFalseAction': self.parse_store_const_action,
            '_AppendAction': self.parse_append_action,
            '_AppendConstAction': self.parse_append_const_action,
            '_SubParsersAction': self.parse_subparsers_action,
        }[action_name]
        fn(action, schema, form)

    def parse_store_action(self, action: argparse.Action, schema: dict, form: list):
        data = {
            'type': self.get_type(action),
        }
        if action.help:
            data['description'] = action.help
        if action.required:
            data['required'] = action.required
        if action.choices:
            data['enum'] = action.choices
        if isinstance(action.type, argparse.FileType):
            form.append({
                'key': action.dest,
                'type': 'file',
            })
        schema[action.dest] = data

    def parse_store_const_action(self, action: argparse.Action, schema: dict, form: list):
        data = {
            'type': 'boolean',
        }
        if action.help:
            data['description'] = action.help
        schema[action.dest] = data

    def parse_append_action(self, action: argparse.Action, schema: dict, form: list):
        data = {
            'type': 'array',
            'items': {
                'type': self.get_type(action),
            },
        }
        if action.help:
            data['description'] = action.help
        schema[action.dest] = data

    def parse_append_const_action(self, action: argparse.Action, schema: dict, form: list):
        data = {
            'type': 'array',
            'items': {
                'type': 'boolean',
            },
        }
        if action.help:
            data['description'] = action.help
        schema[action.dest] = data

    def parse_subparsers_action(self, action: argparse.Action, schema: dict, form: list):
        form.append({
            'type': 'selectfieldset',
            'title': 'Choose command',
            'items': [{'key': name} for name in action.choices],
        })
        for name, subparser in action.choices.items():
            subparser_schema, subparser_form = self.parse_parser(subparser)
            schema[name] = {
                'type': 'object',
                'properties': subparser_schema,
            }
            form.extend(subparser_form)

    def get_type(self, action):
        return 'integer' if action.type is int else 'string'
