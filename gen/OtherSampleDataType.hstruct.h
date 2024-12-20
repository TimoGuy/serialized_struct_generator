/*
 *    ____   _____   _   _   _____   ____       _      _____   _____   ____       ____    ___    ____    _____ 
 *   / ___| | ____| | \ | | | ____| |  _ \     / \    |_   _| | ____| |  _ \     / ___|  / _ \  |  _ \  | ____|
 *  | |  _  |  _|   |  \| | |  _|   | |_) |   / _ \     | |   |  _|   | | | |   | |     | | | | | | | | |  _|  
 *  | |_| | | |___  | |\  | | |___  |  _ <   / ___ \    | |   | |___  | |_| |   | |___  | |_| | | |_| | | |___ 
 *   \____| |_____| |_| \_| |_____| |_| \_\ /_/   \_\   |_|   |_____| |____/     \____|  \___/  |____/  |_____|
 *
 */
#pragma once

#include "hstruct_ifc.h"


struct OtherSampleDataType : public HStruct_ifc
{
    std::string name;
    bool is_enabled;
    uint64_t stride_bytes;

    void serialize_dump(const std::string& fname) override
    {
        SerialBuffer sb;
        write_data_to_serial_buffer(sb);
        bool result{ sb.save_buffer_to_disk(fname) };
        assert(result);
    }

    void serialize_load(const std::string& fname) override
    {
        SerialBuffer sb;
        bool result{ sb.load_buffer_from_disk(fname) };
        assert(result);
        read_data_from_serial_buffer(sb);
    }

    void write_data_to_serial_buffer(SerialBuffer& sb) override
    {
        size_t name__str_length{ name.length() };
        sb.write_elem(&name__str_length, sizeof(size_t));
        sb.write_elem(name.data(), sizeof(char) * name__str_length);
        sb.write_elem(&is_enabled, sizeof(bool));
        sb.write_elem(&stride_bytes, sizeof(uint64_t));
    }

    void read_data_from_serial_buffer(SerialBuffer& sb) override
    {
        size_t name__str_length{
            *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
        };
        name = std::string{ reinterpret_cast<const char*>(sb.read_elem(sizeof(char) * name__str_length)), name__str_length };
        is_enabled = *reinterpret_cast<bool*>(sb.read_elem(sizeof(bool)));
        stride_bytes = *reinterpret_cast<uint64_t*>(sb.read_elem(sizeof(uint64_t)));
    }
};
