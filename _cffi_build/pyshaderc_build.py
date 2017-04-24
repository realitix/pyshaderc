from cffi import FFI
from os import path
import platform


HERE = path.dirname(path.realpath(__file__))
STATIC_LIB_FOLDER = path.join(HERE, 'shaderc_build', 'libshaderc')
LINUX = platform.system() == 'Linux'


# ----------
# BUILD WRAPPER
# ----------
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
l = ['shaderc_combined']

if LINUX:
    l += ['stdc++']

# configure cffi
ffi.cdef(cdef)
ffi.set_source('_pyshaderc', source, libraries=l,
               library_dirs=[STATIC_LIB_FOLDER])


if __name__ == '__main__':
    ffi.compile(verbose=True)
