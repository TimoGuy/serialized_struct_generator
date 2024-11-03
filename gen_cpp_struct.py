from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum

# Arg parser.
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="input .hstruct file to use for generating struct")
args = parser.parse_args()

# Input file structure.
class DataType(Enum):
    UINT8 = 1
    INT8 = 2
    UINT16 = 3
    INT16 = 4
    UINT32 = 5
    INT32 = 6
    UINT64 = 7
    INT64 = 8
    FLOAT = 9
    STRING = 10

@dataclass
class HStruct:
    pass


def main():
    with open(args.filename) as input_file:
        pass

if __name__ == '__main__':
    main()
