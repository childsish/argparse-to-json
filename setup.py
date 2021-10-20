from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name='argparse-to-json',
    version='0.0.1',
    url='https://github.com/childsish/argparse-to-json',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    description='Convert argparse.ArgumentParser to json compatible with JSON Form',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['argparse_to_json'],
)
