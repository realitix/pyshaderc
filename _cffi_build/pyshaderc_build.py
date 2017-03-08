from cffi import FFI
import multiprocessing
from os import path
import os
import platform
import shutil
import sys
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
def clean_build():
    try:
        shutil.rmtree(SHADERC_BIN)
    except:
        pass
    try:
        shutil.rmtree(SHADERC_SRC)
    except:
        pass


def build():
    clean_build()

    # Extract shaderc
    z = ZipFile(SHADERC_ZIP)
    z.extractall(HERE)
    z.close()
    os.makedirs(SHADERC_BIN)

    # Cmake
    shell = sys.platform.startswith('win')
    options = [
        '-DCMAKE_BUILD_TYPE=Release',
        '-DCMAKE_POSITION_INDEPENDENT_CODE=ON',
        '-DSPIRV_SKIP_EXECUTABLES=ON',
        '-DSHADERC_SKIP_TESTS=ON'
    ]

    if platform.system() == 'Windows':
        options += [
            '-DCMAKE_C_FLAGS=" /nologo /EHSC"',
            '-DCMAKE_CXX_FLAGS=" /nologo /EHSC"',
            '-DCMAKE_C_FLAGS_RELEASE=" /nologo /EHSC"',
            '-DCMAKE_CXX_FLAGS_RELEASE=" /nologo /EHSC"'
        ]

    call = ['cmake', '-B'+SHADERC_BIN, '-H'+SHADERC_SRC]
    call += options
    subprocess.check_call(call, stderr=subprocess.STDOUT, shell=shell)

    # make
    cpu = '-j' + str(multiprocessing.cpu_count() * 2)
    subprocess.check_call(['make', cpu, '-C', SHADERC_BIN],
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
l = ['shaderc_combined', 'stdc++']

# configure cffi
ffi.cdef(cdef)
ffi.set_source('_pyshaderc', source, libraries=l,
               library_dirs=[STATIC_LIB_FOLDER])
