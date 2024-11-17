#pragma once

#include <vector>
#include <cassert>


struct SerialBuffer
{
    std::vector<uint8_t> buffer;
    size_t buffer_position{ 0 };

    enum Mode : std::uint8_t
    {
        SBM_READ = 0,
        SBM_WRITE,
    } mode{ 0 };

    // Read buffer methods.
    void* read_elem(size_t elem_bytes)
    {
        assert(mode == SBM_READ);
        void* elem = &buffer[buffer_position];
        buffer_position += elem_bytes;

        return elem;
    }
    // @NOTE: it'll have to be carried out manually in the code to read arrays. First read a uint32_t elem and then read a big chunk and create a vector from the big chunk (https://www.geeksforgeeks.org/how-to-convert-an-array-to-a-vector-in-cpp/#)

    // Write buffer methods.
    void write_elem(void* elem, size_t elem_bytes)
    {
        assert(mode == SBM_WRITE);
        buffer.resize(buffer.size() + elem_bytes);
        std::memcpy(
            buffer.data() + buffer.size() - elem_bytes,
            elem,
            elem_bytes
        );
    }
    // @NOTE: can write big arrays by providing vector.data() as the void* elem, but the beginning number must be written as a uint32_t first.
};
