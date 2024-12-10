#include <iostream>
#include "SampleDataType.hstruct.h"


int main()
{
    std::cout << "Hello World!\n";





    SampleDataType obj{};
#define DO_WRITE 0
#if DO_WRITE
    obj.is_enabled = true;
    obj.sdr_luminance = 243ui8;
    obj.some_signed_char = 122i8;
    obj.id = 33333ui16;
    obj.idk_what_this_could_be = 8888i16;
    obj.complexity = 5555555ui32;
    obj.some_rando_value = -1234567i32;
    obj.memory_pos = 99999999999999ui64;
    obj.grid_pos = -1234567890123i64;
    obj.slider_pos = 0.69f;
    obj.name = "The sunlight strikes the rainbow and makes a rainbow.";
    obj.tokens.emplace_back("Token1 is Tolkien");
    obj.greeting_and_response[0] = "So I know this puppy.";
    obj.greeting_and_response[1] = "That's wonderful! Do tell.";
    obj.ipv4_addresses.clear();
    obj.ipv4_addresses.reserve(2);
    obj.ipv4_addresses.emplace_back(55550);
    obj.ipv4_addresses.emplace_back(55551);
    obj.banana_indexes[0] = 321000;
    obj.banana_indexes[1] = 321001;
    obj.banana_indexes[2] = 321002;
    obj.banana_indexes[3] = 321003;
    obj.banana_indexes[4] = 321004;
    obj.banana_indexes[5] = 321005;
    obj.banana_indexes[6] = 321006;
    obj.banana_indexes[7] = 321007;
    obj.parent_obj.name = "Im PParental unit.";
    obj.parent_obj.is_enabled = false;
    obj.parent_obj.stride_bytes = 5099929201ui64;
    obj.children_objs.clear();
    obj.children_objs.resize(1);
    obj.children_objs[0].name = "Im child 0.";
    obj.children_objs[0].is_enabled = true;
    obj.children_objs[0].stride_bytes = 234555ui64;
    obj.banana_objs[0].name = "Im bananananananana 0.";
    obj.banana_objs[0].is_enabled = false;
    obj.banana_objs[0].stride_bytes = 88383ui64;
    obj.banana_objs[1].name = "Im bananananananana 1.";
    obj.banana_objs[1].is_enabled = true;
    obj.banana_objs[1].stride_bytes = 45543ui64;
    obj.serialize_dump("jojojojojojo.bin");
#else
    obj.serialize_load("jojojojojojo.bin");
    obj;
#endif  // DO_WRITE
}
