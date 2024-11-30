#pragma once

#include <vector>
#include <string>
#include <cassert>
#include <fstream> // For disk ops.

// Make sure is always dealing in little endian.
#if _DEBUG
#include <bit>
static_assert(std::endian::native == std::endian::little);
#endif


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

    // Save to/Load from disk methods.
    bool save_buffer_to_disk(const std::string& fname)
    {
        // Open file for writing.
        std::ofstream file{ fname.c_str(), std::ios::out | std::ios::trunc | std::ios::binary };
        if (!file.is_open())
        {
            return false;
        }

        // Write buffer to file.
        file.write(reinterpret_cast<char*>(buffer.data()), buffer.size());
        file.close();

        // Check for writing errors.
        if (!file.good())
        {
            return false;
        }

        return true;
    }

    bool load_buffer_from_disk(const std::string& fname)
    {
        // Open file for reading.
        std::ifstream file{ fname.c_str(), std::ios::in | std::ios::ate | std::ios::binary };
        if (!file.is_open())
        {
            return false;
        }

        // Get filesize and copy file contents into buffer.
        size_t filesize{ file.tellg() };
        buffer.clear();
        buffer.resize(filesize);
        file.seekg(0);
        file.read(reinterpret_cast<char*>(buffer.data()), filesize);
        file.close();

        // Check for reading errors.
        if (!file.good())
        {
            return false;
        }

        return true;
    }
};
