#pragma once

#include <vector>
#include "hstruct_ifc.h"
#include "OtherSampleDataType.hstruct.h"


struct SampleDataType : public HStruct_ifc
{
    bool                  is_enabled;
    uint8_t                          sdr_luminance;
    int8_t                           some_signed_char;
    uint16_t                         id;
    int16_t                          idk_what_this_could_be;
    uint32_t                         complexity;
    int32_t                          some_rando_value;
    uint64_t                         memory_pos;
    int64_t                          grid_pos;
    float_t                          slider_pos;
    std::string                      name;
    std::vector<uint32_t>            ipv4_addresses;
    OtherSampleDataType              parent_obj;
    std::vector<OtherSampleDataType> children_objs;

    void serialize_dump(const std::string& fname) override
    {
        
    }

    void serialize_load(const std::string& fname) override
    {

    }


};
