#pragma once

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
