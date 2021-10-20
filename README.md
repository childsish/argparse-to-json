# argparse-to-json
Convert Python argparse parsers to json compatible with [JSON Form](https://github.com/jsonform/jsonform).

## Usage

```python
import argparse

from argparse_to_json import convert_parser_to_json

parser = argparse.ArgumentParser()
parser.add_argument('input')
json_schema = convert_parser_to_json(parser)
```

See the `example` folder for a [Flask](https://flask.palletsprojects.com) app that renders forms for command line interfaces using [JSON Form](https://github.com/jsonform/jsonform). You can run the example as follows:

```shell
pip install flask
FLASK_APP=app.py
flask run
```

## Why?

Because maybe I wanted to have a simple way to create GUIs for my Python CLI's.
