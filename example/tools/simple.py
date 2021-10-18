import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input1', help='Add input')
    parser.add_argument('-i', '--input2', help='Add even more input')
    parser.add_argument('-s', '--select', choices=['Alpha', 'Beta', 'Gamma', 'Delta'])
    return parser
