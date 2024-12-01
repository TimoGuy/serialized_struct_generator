/*
 *    ____   _____   _   _   _____   ____       _      _____   _____   ____       ____    ___    ____    _____ 
 *   / ___| | ____| | \ | | | ____| |  _ \     / \    |_   _| | ____| |  _ \     / ___|  / _ \  |  _ \  | ____|
 *  | |  _  |  _|   |  \| | |  _|   | |_) |   / _ \     | |   |  _|   | | | |   | |     | | | | | | | | |  _|  
 *  | |_| | | |___  | |\  | | |___  |  _ <   / ___ \    | |   | |___  | |_| |   | |___  | |_| | | |_| | | |___ 
 *   \____| |_____| |_| \_| |_____| |_| \_\ /_/   \_\   |_|   |_____| |____/     \____|  \___/  |____/  |_____|
 *
 */
#pragma once

#include <array>
#include <string>
#include <vector>
#include "SerialBuffer.h"

// Make sure is always dealing in little endian.
#if _DEBUG
#include <version>
static_assert(__cplusplus >= 202002L);
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
