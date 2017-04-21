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
    if not path.exists(SHADERC_SRC):
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
            '-DCMAKE_C_FLAGS=/nologo /EHsc /MD',
            '-DCMAKE_CXX_FLAGS=/nologo /EHsc /MD',
            '-DCMAKE_C_FLAGS_RELEASE=/nologo /EHsc /MD',
            '-DCMAKE_CXX_FLAGS_RELEASE=/nologo /EHsc /MD',
            '-DSHADERC_ENABLE_SHARED_CRT=ON'
        ]

    call = ['cmake', '-B'+SHADERC_BIN, '-H'+SHADERC_SRC]
    call += options
    subprocess.check_call(call, stderr=subprocess.STDOUT, shell=shell)

    # Build
    cpu = ''
    if platform.system() == 'Linux':
        cpu = '-j' + str(multiprocessing.cpu_count() * 2)

    subprocess.check_call(['cmake', '--build', SHADERC_BIN, '--config',
                          'Release', '--', cpu], stderr=subprocess.STDOUT,
                          shell=shell)


if __name__ == '__main__':
    build()
