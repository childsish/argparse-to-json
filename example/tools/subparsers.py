import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparser1 = subparsers.add_parser('subparser1')
    subparser1.add_argument('input1', help='First input of subparser1')
    subparser2 = subparsers.add_parser('subparser2')
    subparser2.add_argument('input2', help='First input of subparser2', type=int)
    subparser3 = subparsers.add_parser('subparser3')
    subparser3.add_argument('input3', help='First input of subparser3', choices=['Alpha', 'Beta', 'Gamma', 'Delta'])
    return parser
