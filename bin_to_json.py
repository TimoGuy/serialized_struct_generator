from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum

# Arg parser.
parser = ArgumentParser()
parser.add_argument("-f", "--hstruct-file", dest="hstruct_fname", required=True,
                    help="input .hstruct file to use as schema")
parser.add_argument("-b", "--bin-file", dest="bin_fname", required=True,
                    help="input binary file to convert to JSON")
args = parser.parse_args()


def main():
    pass

if __name__ == '__main__':
    main()
