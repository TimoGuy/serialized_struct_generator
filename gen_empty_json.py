from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum

# Arg parser.
parser = ArgumentParser()
parser.add_argument("-f", "--hstruct-file", dest="hstruct_fname", required=True,
                    help="input .hstruct file to use as schema")
parser.add_argument("-d", "--json-data-file", dest="json_fname", required=True,
                    help="input JSON file to convert to binary")
args = parser.parse_args()


def main():
    pass

if __name__ == '__main__':
    main()
