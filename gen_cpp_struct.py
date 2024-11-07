from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List, Tuple
import re
# from enum import Enum

# Arg parser.
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="input .hstruct file to use for generating struct")
args = parser.parse_args()

# Input file structure.


# class DataType(Enum):
#     BOOL = 0
#     UINT8 = 1
#     INT8 = 2
#     UINT16 = 3
#     INT16 = 4
#     UINT32 = 5
#     INT32 = 6
#     UINT64 = 7
#     INT64 = 8
#     FLOAT = 9
#     STRING = 10
#     LIST = 11
#     STRUCT = 12


all_primitive_names = [
    'bool', 'uint8', 'int8', 'uint16', 'int16', 'uint32', 'int32', 'uint64', 'int64', 'float', 'string'
]


class DataType:
    type_name: str
    is_builtin_primitive: bool
    is_list_of_type: bool
    list_count: int  # If -1 then list becomes std::vector. If 0, then fail. If >0, then list becomes std::array.

    def __init__(self, type_token: str):
        # Check if type is a list.
        type_str_stem = ''
        list_count = -1
        if type_token[-1] == ']':
            is_list_of_type = True

            # Check if list is finite or expandable.
            lb_pos = type_token.find('[')
            assert lb_pos > 0, f'Malformed type: {type_token}'

            list_finite_count_str = type_token[lb_pos + 1 : -2].strip()
            if len(list_finite_count_str) > 0:
                list_count = int(list_finite_count_str)
                assert list_count > 0, f'Bad list count: {list_count}'

            type_str_stem = type_token[:lb_pos]
        else:
            is_list_of_type = False
            type_str_stem = type_token

        # Simple check that there aren't any special characters in cleaned token str.
        assert re.compile(r"\W").match(type_str_stem) is None, f'Malformed type: {type_token}'

        # Finish.
        self.type_name = type_str_stem
        self.is_builtin_primitive = bool(type_str_stem in all_primitive_names)
        self.is_list_of_type = is_list_of_type
        self.list_count = list_count


def parse_line(file_line: str) -> Tuple[DataType, str]:
    comment_sym = file_line.find('#')
    if comment_sym >= 0:
        file_line = file_line[:comment_sym]
    tokens = file_line.split()

    num_tokens = len(tokens)
    if num_tokens == 0:
        return None, None
    assert num_tokens == 2, f'Improper number of tokens for line: `{file_line}`'

    line_type = DataType(tokens[0])
    variable_name = tokens[1]
    return line_type, variable_name


@dataclass
class HStruct:
    members: List[DataType]


# Generated header comment marking generated code.
generated_code_comment_code = \
"""/*
 *    ____   _____   _   _   _____   ____       _      _____   _____   ____       ____    ___    ____    _____ 
 *   / ___| | ____| | \ | | | ____| |  _ \     / \    |_   _| | ____| |  _ \     / ___|  / _ \  |  _ \  | ____|
 *  | |  _  |  _|   |  \| | |  _|   | |_) |   / _ \     | |   |  _|   | | | |   | |     | | | | | | | | |  _|  
 *  | |_| | | |___  | |\  | | |___  |  _ <   / ___ \    | |   | |___  | |_| |   | |___  | |_| | | |_| | | |___ 
 *   \____| |_____| |_| \_| |_____| |_| \_\ /_/   \_\   |_|   |_____| |____/     \____|  \___/  |____/  |_____|
 *
 */
"""

# HStruct interface.
hstruct_ifc_code = \
"""#pragma once

#include <string>


class HStruct_ifc
{
public:
    // Dumps HStruct into binary serialization, writing the contents
    // out to the file `fname`.
    virtual void serialize_dump(const std::string& fname) = 0;

    // Loads HStruct from a binary serialization at `fname`.
    virtual void serialize_load(const std::string& fname) = 0;
};
"""


def main():
    #TESTS######
    asdf = DataType("OtherSampleDataType[]")
    parse_line("         int64[]    jojo # I need a nap yo")
    #ENDTESTS###

    with open(args.filename) as input_file:
        pass

if __name__ == '__main__':
    main()
