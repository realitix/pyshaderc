from cffi import FFI
from os import path

HERE = path.dirname(path.realpath(__file__))

ffi = FFI()

# read file
with open(path.join(HERE, 'shaderc.h')) as f:
    raw_header = f.read()

# prepare cdef and source
cdef = raw_header
cdef += """
extern "Python" shaderc_include_result* resolve_callback(
    void*, const char*, int, const char*, size_t);

extern "Python" void release_callback(void*, shaderc_include_result*);
"""

source = """
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
"""
source += raw_header

# libraries path
l = ['shaderc_combined', 'stdc++']

# configure cffi
ffi.cdef(cdef)
ffi.set_source('_pyshaderc', source, libraries=l, library_dirs=[HERE])
