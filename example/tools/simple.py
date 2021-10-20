import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input1', metavar='Input 1', help='String input')
    parser.add_argument('-i', '--input2', metavar='Input 2', type=int, help='Integer input')
    parser.add_argument('-s', '--select', metavar='Select Greek letter', choices=['Alpha', 'Beta', 'Gamma', 'Delta'])
    return parser
