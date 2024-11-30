import re
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List, Tuple, Dict
from pathlib import Path

# Arg parser.
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="input .hstruct file to use for generating struct")
args = parser.parse_args()

# Input file structure.
all_primitive_names_to_cpp_type: Dict[str, str] = {
    'bool': 'bool',
    'uint8': 'uint8_t',
    'int8': 'int8_t',
    'uint16': 'uint16_t',
    'int16': 'int16_t',
    'uint32': 'uint32_t',
    'int32': 'int32_t',
    'uint64': 'uint64_t',
    'int64': 'int64_t',
    'float': 'float_t',
    'string': 'std::string',
}


INDENTATION_AMOUNT = 4
class CppFilePrinter:

    def __init__(self, fname: str):
        self.fname = fname
        self.indentation = 0

    def __enter__(self):
        self.fhandle = open(self.fname, "w")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fhandle.close()

    def write_line(self, line: str):
        if len(line.strip()) == 0:
            # Write empty line if no content.
            line_with_indent = ""
        else:
            allow_indentation_mutation = True
            if "{" in line and "}" in line:
                # Don't mess with indentation
                allow_indentation_mutation = False

            # Check for end block.
            if allow_indentation_mutation and "}" in line:
                assert self.indentation >= INDENTATION_AMOUNT, "One too many exit blocks!"
                self.indentation -= INDENTATION_AMOUNT

            # Construct indentation amount.
            indent = " " * self.indentation

            # Check for start block.
            if allow_indentation_mutation and "{" in line:
                self.indentation += INDENTATION_AMOUNT

            # Combine indent with line content.
            line_with_indent = f"{indent}{line}"
        
        # Write out line.
        self.fhandle.write(f"{line_with_indent}\n")


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

            list_finite_count_str = type_token[lb_pos + 1 : -1].strip()
            if len(list_finite_count_str) > 0:
                list_count = int(list_finite_count_str)
                assert list_count > 0, f'Bad list count: {list_count}'

            type_str_stem = type_token[:lb_pos]
        else:
            is_list_of_type = False
            type_str_stem = type_token

        is_builtin_primitive = bool(type_str_stem in all_primitive_names_to_cpp_type.keys())
        type_name_cpp = (all_primitive_names_to_cpp_type[type_str_stem] if is_builtin_primitive else type_str_stem)

        # Simple check that there aren't any special characters in cleaned token str.
        assert re.compile(r"\W").match(type_str_stem) is None, f'Malformed type: {type_token}'

        # Finish.
        self.type_name = type_name_cpp
        self.is_builtin_primitive = is_builtin_primitive
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


def field_type_name_to_cpp_name(field_type: DataType):
    type_name = field_type.type_name
    if field_type.is_list_of_type:
        assert field_type.list_count != 0, "Malformed list_count"
        if field_type.list_count == -1:
            type_name = f"std::vector<{field_type.type_name}>"
        else:
            type_name = f"std::array<{field_type.type_name}, {field_type.list_count}>"
    return type_name


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

#include <array>
#include <string>
#include <vector>
#include "SerialBuffer.h"

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

protected:
    // Internal act of collection of data to SerialBuffer.
    virtual void write_data_to_serial_buffer(SerialBuffer& buffer) = 0;

    // Internal propagation of data to HStruct.
    virtual void read_data_from_serial_buffer(SerialBuffer& buffer) = 0;
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

    # Write out generated file.
    with CppFilePrinter(f"gen/{fname_only}.h") as cfp:
        cfp.write_line(GENERATED_CODE_COMMENT_CODE)
        cfp.write_line("#pragma once")
        cfp.write_line("")
        cfp.write_line("#include \"hstruct_ifc.h\"")

        for import_em in import_list:
            cfp.write_line(f"#include \"{import_em}.hstruct.h\"")

        cfp.write_line("")
        cfp.write_line("")


        for struct in struct_list:
            # Start struct.
            cfp.write_line(f"struct {struct.struct_name} : public HStruct_ifc")
            cfp.write_line("{")

            # Write out member variables.
            for member in struct.members:
                cfp.write_line(f"{field_type_name_to_cpp_name(member.field_type)} {member.field_name};")

            cfp.write_line("")


            # serialize_dump().
            cfp.write_line("void serialize_dump(const std::string& fname) override")
            cfp.write_line("{")

            # Dump struct data into buffer.
            cfp.write_line("SerialBuffer sb;")
            cfp.write_line("write_data_to_serial_buffer(sb);")

            # Write data to disk.
            cfp.write_line("bool result{ sb.save_buffer_to_disk(fname) };")
            cfp.write_line("assert(result);")
            cfp.write_line("}")
            cfp.write_line("")


            # serialize_load().
            cfp.write_line("void serialize_load(const std::string& fname) override")
            cfp.write_line("{")

            # Read data from disk.
            cfp.write_line("SerialBuffer sb;")
            cfp.write_line("bool result{ sb.load_buffer_from_disk(fname) };")
            cfp.write_line("assert(result);")
            cfp.write_line("read_data_from_serial_buffer(sb);")

            cfp.write_line("}")
            cfp.write_line("")


            # write_data_to_serial_buffer().
            cfp.write_line("void write_data_to_serial_buffer(SerialBuffer& sb) override")
            cfp.write_line("{")

            # Write out member variables.
            for member in struct.members:
                iterations = 1  # Default 1 for if not a list.
                if member.field_type.is_list_of_type:
                    if member.field_type.list_count == -1:
                        # Is vector, write count as int right now.
                        cfp.write_line(f"size_t {member.field_name}__list_count{{ {member.field_name}.size() }};")
                        cfp.write_line(f"sb.write_elem(&{member.field_name}__list_count, sizeof(size_t));")
                        iterations = f"{member.field_name}__list_count"
                    else:
                        # Is array, use fixed count.
                        iterations = member.field_type.list_count
                        assert iterations > 0, f"Bad list_count: {iterations}"

                # Write out elements.
                field_suffix = ""
                if iterations != 1:
                    cfp.write_line(f"for (size_t i = 0; i < {iterations}; i++)")
                    cfp.write_line("{")
                    field_suffix = "[i]"
                if member.field_type.is_builtin_primitive:
                    # Write primitive.
                    cfp.write_line(f"sb.write_elem(&{member.field_name}{field_suffix}, sizeof({member.field_type.type_name}));")
                else:
                    # Recurse thru HStruct write func.
                    cfp.write_line(f"{member.field_name}{field_suffix}.write_data_to_serial_buffer(sb);")
                if iterations != 1:
                    cfp.write_line("}")
                    cfp.write_line("")


            cfp.write_line("}")
            cfp.write_line("")


            # read_data_from_serial_buffer().
            cfp.write_line(f"void read_data_from_serial_buffer(SerialBuffer& sb) override")
            cfp.write_line("{")

            # Read in member variables.
            for member in struct.members:
                iterations = 1  # Default 1 for if not a list.
                if member.field_type.is_list_of_type:
                    if member.field_type.list_count == -1:
                        # Is vector, read count as int right now.
                        cfp.write_line(f"size_t {member.field_name}__list_count{{")
                        cfp.write_line(f"*reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))")
                        cfp.write_line("};")
                        iterations = f"{member.field_name}__list_count"
                    else:
                        # Is array, use fixed count.
                        iterations = member.field_type.list_count
                        assert iterations > 0, f"Bad list_count: {iterations}"

                # Write out elements.
                field_suffix = ""
                if iterations != 1:
                    cfp.write_line(f"for (size_t i = 0; i < {iterations}; i++)")
                    cfp.write_line("{")
                    field_suffix = "[i]"
                if member.field_type.is_builtin_primitive:
                    # Read primitive.
                    # @TODO: fix `field_suffix` assignment to use `emplace_back()` if a vector (not required for fixed size std::array)
                    cfp.write_line(f"{member.field_name}{field_suffix} = *reinterpret_cast<{member.field_type.type_name}*>(sb.read_elem(sizeof({member.field_type.type_name})));")
                else:
                    # Recurse thru HStruct read func.
                    cfp.write_line(f"{member.field_name}{field_suffix}.read_data_from_serial_buffer(sb);")
                if iterations != 1:
                    cfp.write_line("}")
                    cfp.write_line("")

            cfp.write_line("}")

            # End struct.
            cfp.write_line("};")


    # End.
    pass

if __name__ == '__main__':
    main()
