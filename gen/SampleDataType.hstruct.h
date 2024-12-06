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
#include "OtherSampleDataType.hstruct.h"


struct SampleDataType : public HStruct_ifc
{
    bool is_enabled;
    uint8_t sdr_luminance;
    int8_t some_signed_char;
    uint16_t id;
    int16_t idk_what_this_could_be;
    uint32_t complexity;
    int32_t some_rando_value;
    uint64_t memory_pos;
    int64_t grid_pos;
    float_t slider_pos;
    std::string name;
    std::vector<std::string> tokens;
    std::array<std::string, 2> greeting_and_response;
    std::vector<uint32_t> ipv4_addresses;
    std::array<uint32_t, 8> banana_indexes;
    OtherSampleDataType parent_obj;
    std::vector<OtherSampleDataType> children_objs;
    std::array<OtherSampleDataType, 2> banana_objs;

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
        sb.write_elem(&is_enabled, sizeof(bool));
        sb.write_elem(&sdr_luminance, sizeof(uint8_t));
        sb.write_elem(&some_signed_char, sizeof(int8_t));
        sb.write_elem(&id, sizeof(uint16_t));
        sb.write_elem(&idk_what_this_could_be, sizeof(int16_t));
        sb.write_elem(&complexity, sizeof(uint32_t));
        sb.write_elem(&some_rando_value, sizeof(int32_t));
        sb.write_elem(&memory_pos, sizeof(uint64_t));
        sb.write_elem(&grid_pos, sizeof(int64_t));
        sb.write_elem(&slider_pos, sizeof(float_t));
        size_t name__str_length{ name.length() };
        sb.write_elem(&name__str_length, sizeof(size_t));
        sb.write_elem(name.data(), sizeof(char) * name__str_length);

        size_t tokens__list_count{ tokens.size() };
        sb.write_elem(&tokens__list_count, sizeof(size_t));
        for (size_t i = 0; i < tokens__list_count; i++)
        {
            size_t tokens__str_length{ tokens[i].length() };
            sb.write_elem(&tokens__str_length, sizeof(size_t));
            sb.write_elem(tokens[i].data(), sizeof(char) * tokens__str_length);
        }

        for (size_t i = 0; i < 2; i++)
        {
            size_t greeting_and_response__str_length{ greeting_and_response[i].length() };
            sb.write_elem(&greeting_and_response__str_length, sizeof(size_t));
            sb.write_elem(greeting_and_response[i].data(), sizeof(char) * greeting_and_response__str_length);
        }

        size_t ipv4_addresses__list_count{ ipv4_addresses.size() };
        sb.write_elem(&ipv4_addresses__list_count, sizeof(size_t));
        for (size_t i = 0; i < ipv4_addresses__list_count; i++)
        {
            sb.write_elem(&ipv4_addresses[i], sizeof(uint32_t));
        }

        for (size_t i = 0; i < 8; i++)
        {
            sb.write_elem(&banana_indexes[i], sizeof(uint32_t));
        }

        parent_obj.write_data_to_serial_buffer(sb);

        size_t children_objs__list_count{ children_objs.size() };
        sb.write_elem(&children_objs__list_count, sizeof(size_t));
        for (size_t i = 0; i < children_objs__list_count; i++)
        {
            children_objs[i].write_data_to_serial_buffer(sb);
        }

        for (size_t i = 0; i < 2; i++)
        {
            banana_objs[i].write_data_to_serial_buffer(sb);
        }
    }

    void read_data_from_serial_buffer(SerialBuffer& sb) override
    {
        is_enabled = *reinterpret_cast<bool*>(sb.read_elem(sizeof(bool)));
        sdr_luminance = *reinterpret_cast<uint8_t*>(sb.read_elem(sizeof(uint8_t)));
        some_signed_char = *reinterpret_cast<int8_t*>(sb.read_elem(sizeof(int8_t)));
        id = *reinterpret_cast<uint16_t*>(sb.read_elem(sizeof(uint16_t)));
        idk_what_this_could_be = *reinterpret_cast<int16_t*>(sb.read_elem(sizeof(int16_t)));
        complexity = *reinterpret_cast<uint32_t*>(sb.read_elem(sizeof(uint32_t)));
        some_rando_value = *reinterpret_cast<int32_t*>(sb.read_elem(sizeof(int32_t)));
        memory_pos = *reinterpret_cast<uint64_t*>(sb.read_elem(sizeof(uint64_t)));
        grid_pos = *reinterpret_cast<int64_t*>(sb.read_elem(sizeof(int64_t)));
        slider_pos = *reinterpret_cast<float_t*>(sb.read_elem(sizeof(float_t)));
        size_t name__str_length{
            *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
        };
        name = std::string{ reinterpret_cast<const char*>(sb.read_elem(sizeof(char) * name__str_length)), name__str_length };

        size_t tokens__list_count{
            *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
        };
        tokens.clear();
        tokens.reserve(tokens__list_count);
        for (size_t i = 0; i < tokens__list_count; i++)
        {
            size_t tokens__str_length{
                *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
            };
            tokens.emplace_back(reinterpret_cast<const char*>(sb.read_elem(sizeof(char) * tokens__str_length)), tokens__str_length);
        }

        for (size_t i = 0; i < 2; i++)
        {
            size_t greeting_and_response__str_length{
                *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
            };
            greeting_and_response[i] = std::string{ reinterpret_cast<const char*>(sb.read_elem(sizeof(char) * greeting_and_response__str_length)), greeting_and_response__str_length };
        }

        size_t ipv4_addresses__list_count{
            *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
        };
        ipv4_addresses.clear();
        ipv4_addresses.reserve(ipv4_addresses__list_count);
        for (size_t i = 0; i < ipv4_addresses__list_count; i++)
        {
            ipv4_addresses.emplace_back(*reinterpret_cast<uint32_t*>(sb.read_elem(sizeof(uint32_t))));
        }

        for (size_t i = 0; i < 8; i++)
        {
            banana_indexes[i] = *reinterpret_cast<uint32_t*>(sb.read_elem(sizeof(uint32_t)));
        }

        parent_obj.read_data_from_serial_buffer(sb);

        size_t children_objs__list_count{
            *reinterpret_cast<size_t*>(sb.read_elem(sizeof(size_t)))
        };
        children_objs.clear();
        children_objs.reserve(children_objs__list_count);
        for (size_t i = 0; i < children_objs__list_count; i++)
        {
            children_objs.emplace_back(OtherSampleDataType{});
            children_objs.back().read_data_from_serial_buffer(sb);
        }

        for (size_t i = 0; i < 2; i++)
        {
            banana_objs[i].read_data_from_serial_buffer(sb);
        }
    }
};
