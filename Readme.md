# Serialized Struct Generator

> A simple python tool that generates a serializable struct from an `.hstruct` file

## C++ Struct Generation

Using a `.hstruct` file as input, a C++ struct gets generated and placed into a header
file. Alongside this set of header files is an interface header file where the base is
for the serialization/deserialization virtual functions (bin<->struct only).


## Binary file <-> JSON file

This tool will be able to take an `.hstruct` file and a binary file as input to create
a JSON file with the schema of the `.hstruct` file and data of the binary file.

Using a JSON file and `.hstruct` file as input, a binary file can get created.

Of course, error checking to see if the schema of the binary file and JSON match the
schema of the `.hstruct` file.

This is essentially for data editing for dummies, plus debugging if needed.
