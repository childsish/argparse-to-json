import os
import importlib

from flask import Flask, jsonify, render_template
from argparse_to_json import convert_parser_to_json

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template(
        'index.html',
        tools=[os.path.splitext(tool)[0] for tool in os.listdir('tools') if tool.endswith('.py') and tool != '__init__.py']
    )


@app.route('/tools/<name>', methods=['GET'])
def get_tool(name):
    module = importlib.import_module('tools.{}'.format(name))
    return jsonify(convert_parser_to_json(module.get_parser()))
