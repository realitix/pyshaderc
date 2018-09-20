from cffi import FFI
from os import path
import platform


HERE = path.dirname(path.realpath(__file__))
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
"""
source += raw_header

# libraries path
l = ['shaderc_combined']

if LINUX:
    l += ['stdc++']

# lib folders
f1 = path.join(HERE, 'shaderc_build', 'libshaderc')
f2 = path.join(f1, 'Release')

# configure cffi
ffi.cdef(cdef)
ffi.set_source('_pyshaderc', source, libraries=l,
               library_dirs=[f1, f2])


if __name__ == '__main__':
    ffi.compile(verbose=True)
