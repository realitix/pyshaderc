from cffi import FFI
import multiprocessing
from os import path
import os
import platform
import subprocess
from zipfile import ZipFile


HERE = path.dirname(path.realpath(__file__))
SHADERC_ZIP = path.join(HERE, 'shaderc-cb4f0f6.zip')
SHADERC_SRC = path.join(HERE, 'shaderc')
SHADERC_BIN = path.join(HERE, 'shaderc_build')
STATIC_LIB_FOLDER = path.join(SHADERC_BIN, 'libshaderc')


# ----------
# BUILD STATIC LIB
# ----------
def build():
    # Extract shaderc
    if not path.exists(SHADERC_ZIP):
        z = ZipFile(SHADERC_ZIP)
        z.extractall(HERE)
        z.close()

    if not path.exists(SHADERC_BIN):
        os.makedirs(SHADERC_BIN)

    # Prepare
    shell = platform.system() == 'Windows'
    options = [
        '-DCMAKE_BUILD_TYPE=Release',
        '-DCMAKE_POSITION_INDEPENDENT_CODE=ON',
        '-DSPIRV_SKIP_EXECUTABLES=ON',
        '-DSHADERC_SKIP_TESTS=ON'
    ]

    if platform.system() == 'Windows':
        options += [
            '-DCMAKE_C_FLAGS=/nologo /EHsc',
            '-DCMAKE_CXX_FLAGS=/nologo /EHsc',
            '-DCMAKE_C_FLAGS_RELEASE=/nologo /EHsc',
            '-DCMAKE_CXX_FLAGS_RELEASE=/nologo /EHsc'
        ]

    call = ['cmake', '-B'+SHADERC_BIN, '-H'+SHADERC_SRC]
    call += options
    subprocess.check_call(call, stderr=subprocess.STDOUT, shell=shell)

    # Build
    cpu = ''
    if platform.system() == 'Linux':
        cpu = '-j' + str(multiprocessing.cpu_count() * 2)

    subprocess.check_call(['cmake', '--build', SHADERC_BIN, '--', cpu],
                          stderr=subprocess.STDOUT, shell=shell)


build()


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

# configure cffi
ffi.cdef(cdef)
ffi.set_source('_pyshaderc', source, libraries=l,
               library_dirs=[STATIC_LIB_FOLDER])
