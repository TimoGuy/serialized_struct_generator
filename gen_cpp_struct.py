import re
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List, Tuple
from pathlib import Path

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


@dataclass
class TokenLine:
    indentation_amount: int
    tokens: List[str]


@dataclass
class HField:
    field_type: DataType
    field_name: str


@dataclass
class HStruct:
    struct_name: str
    members: List[HField]


def read_into_token_line(file_line: str) -> TokenLine:
    comment_sym = file_line.find('#')
    if comment_sym >= 0:
        file_line = file_line[:comment_sym]

    line_len = len(file_line)
    line_len_left_trimmed = len(file_line.lstrip())
    indentation_amt = line_len - line_len_left_trimmed

    tokens = file_line.split()
    return TokenLine(indentation_amt, tokens)


def parse_struct_import_token_line(tokens: List[str]) -> str:
    assert len(tokens) == 2, f'Improper number of tokens in list: {tokens}'
    assert tokens[0] == 'import', f'First token isn\'t `import`: {tokens[0]}'
    return tokens[1]


def parse_struct_name_token_line(tokens: List[str]) -> str:
    assert len(tokens) == 2, f'Improper number of tokens in list: {tokens}'
    assert tokens[0] == 'struct', f'First token isn\'t `struct`: {tokens[0]}'
    assert tokens[1][-1] == ':', f'Second token doesn\'t end with `:`: {tokens[1]}'
    return tokens[1][:-1]


def parse_struct_member_field_token_line(tokens: List[str]) -> HField:
    assert len(tokens) == 2, f'Improper number of tokens in list: {tokens}'
    line_type = DataType(tokens[0])
    variable_name = tokens[1]
    return HField(line_type, variable_name)


# Generated header comment marking generated code.
GENERATED_CODE_COMMENT_CODE = \
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
HSTRUCT_IFC_CODE = \
"""#pragma once

#include <string>

// Make sure is always dealing in little endian.
#if _DEBUG
#include <bit>
static_assert(std::endian::native == std::endian::little);
#endif


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
    # asdf = DataType("OtherSampleDataType[]")
    # parse_line("         int64[]    jojo # I need a nap yo")
    #ENDTESTS###

    # Read in all tokens.
    lines: List[TokenLine] = []

    with open(args.filename, "r") as input_file:
        for line in input_file:
            token_line = read_into_token_line(line)
            if len(token_line.tokens) > 0:
                lines.append(token_line)
    
    # Group read lines into groups based off indentation amount.
    line_groups: List[List[TokenLine]] = []
    for line in lines:
        if line.indentation_amount == 0:
            line_groups.append([line,])
        else:
            line_groups[-1].append(line)

    # Turn token groups into structs.
    import_list: List[str] = []
    struct_list: List[HStruct] = []
    for group in line_groups:
        # Add import to import list.
        initial_token = group[0].tokens[0]
        if initial_token == 'import':
            # Parse out import statement.
            import_list.append(
                parse_struct_import_token_line(group[0].tokens)
            )
        elif initial_token == 'struct':
            # Iterate thru struct members.
            struct_name = ''
            struct_members: List[HField] = []
            first = True
            for token_line in group:
                if first:
                    struct_name = parse_struct_name_token_line(token_line.tokens)
                    first = False
                else:
                    struct_members.append(
                        parse_struct_member_field_token_line(token_line.tokens)
                    )
            struct_list.append(
                HStruct(struct_name, struct_members)
            )

    # Make sure only one struct definition is there.
    assert len(struct_list) == 1, "Only place 1 struct definition."

    # Make sure struct is same definition as file.
    fname_only = Path(args.filename).name
    msg = f"Struct name must match file name. " \
        f"Struct name: {struct_list[0].struct_name}. File name: {fname_only}."
    assert fname_only == f"{struct_list[0].struct_name}.hstruct", msg

    # Write out generated file. @DEBUG: just gonna print stuff out for now.
    print(GENERATED_CODE_COMMENT_CODE)
    print("#pragma once")
    print("")
    print("#include \"hstruct_ifc.h\"")

    for import_em in import_list:
        print(f"#include \"{import_em}.hstruct.h\"")

    print("")
    print("")

    for struct in struct_list:
        print(f"struct {struct.struct_name} : public HStruct_ifc")
        print("{")

        # Write out member variables.
        for member in struct.members:
            member.field_type # @TODO: START HERE!!!! MAKE THE ACTUAL hstruct FIELD TYPE TO c++ FIELD TYPE CONVERSION!
            print(f"{member.field_type.type_name} {member.field_name};")

        print("};")
        print("")


    # End.
    pass

if __name__ == '__main__':
    main()
