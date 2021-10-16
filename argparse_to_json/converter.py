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
        self.parse_store_action(action, schema, form) if action_name == '_StoreAction' else\
            self.parse_store_true_action(action, schema, form) if action_name == '_StoreTrueAction' else\
            self.parse_subparsers_action(action, schema, form) if action_name == '_SubParsersAction' else\
            None

    def parse_store_action(self, action: argparse.Action, schema: dict, form: list):
        data = {
            'type': 'string'
        }
        if action.help:
            data['description'] = action.help
        if action.required:
            data['required'] = action.required
        if action.choices:
            data['enum'] = action.choices
        schema[action.dest] = data

    def parse_store_true_action(self, action: argparse.Action, schema: dict, form: list):
        data = {
            'type': 'boolean',
        }
        if action.help:
            data['description'] = action.help
        schema[action.dest] = data

    def parse_subparsers_action(self, action: argparse.Action, schema: dict, form: list):
        form.append({
            'type': 'selectFieldSet',
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
