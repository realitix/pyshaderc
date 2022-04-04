import multiprocessing
from os import path, environ
import os
import platform
import subprocess
from zipfile import ZipFile
import shutil

WINDOWS = platform.system() == "Windows"
MACOS   = platform.system() == "Darwin"
LINUX   = platform.system() == "Linux"

HERE = path.dirname(path.realpath(__file__))
SHADERC_ZIP = path.join(HERE, 'shaderc-cb4f0f6.zip')
SHADERC_SRC = path.join(HERE, 'shaderc')
SHADERC_BIN = path.join(HERE, 'shaderc_build')
STATIC_LIB_FOLDER = path.join(SHADERC_BIN, 'libshaderc')

def get_vulkan_sdk_lib():
    if "VULKAN_SDK" in environ.keys():
        if LINUX or MACOS:
            fvulkan = path.join(environ["VULKAN_SDK"], "lib", "shaderc_combined.a")
            if path.exists(fvulkan):
                print("Found shaderc_combined in Vulkan SDK: '%s'" % fvulkan)
                return fvulkan
            
        elif WINDOWS:
            fvulkan = path.join(environ["VULKAN_SDK"], "Lib", "shaderc_combined.lib")
            if path.exists(fvulkan):
                print("Found shaderc_combined in Vulkan SDK: '%s'" % fvulkan)
                return fvulkan
    
    print("Could not find shaderc_combined in Vulkan SDK, VULKAN_SDK: '%s'" % environ.get("VULKAN_SDK", ""))
    return None

def vulkan_sdk_fallback():
    vulkan_sdk_lib_path = get_vulkan_sdk_lib()
    if vulkan_sdk_lib_path is not None: 
        static_lib_path = path.join(STATIC_LIB_FOLDER, path.basename(vulkan_sdk_lib_path))
        os.makedirs(STATIC_LIB_FOLDER, exist_ok=True)

        print("Copying '%s' to '%s'" % (vulkan_sdk_lib_path, static_lib_path))
        shutil.copy(vulkan_sdk_lib_path, static_lib_path)
        if path.exists(static_lib_path):
            return True
        else:
            print("Failed to copy library from '%s' to '%s'" % (vulkan_sdk_lib_path, static_lib_path))
    
    return False

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
    options = [
        '-DCMAKE_BUILD_TYPE=Release',
        '-DCMAKE_POSITION_INDEPENDENT_CODE=ON',
        '-DSPIRV_SKIP_EXECUTABLES=ON',
        '-DSHADERC_SKIP_TESTS=ON'
    ]

    if WINDOWS:
        options += [
            '-DCMAKE_C_FLAGS=/nologo /EHsc /MD',
            '-DCMAKE_CXX_FLAGS=/nologo /EHsc /MD',
            '-DCMAKE_C_FLAGS_RELEASE=/nologo /EHsc /MD',
            '-DCMAKE_CXX_FLAGS_RELEASE=/nologo /EHsc /MD',
            '-DSHADERC_ENABLE_SHARED_CRT=ON'
        ]

    call = ['cmake', '-B'+SHADERC_BIN, '-H'+SHADERC_SRC]
    call += options

    try:
        subprocess.check_call(call, stderr=subprocess.STDOUT, shell=WINDOWS)
    except subprocess.CalledProcessError as e:
        # If CMake fails to configure, we revert to attempt to use Vulkan SDK
        if not vulkan_sdk_fallback():
            raise e
        else:
            return

    # Build
    cpu = ''
    if platform.system() == 'Linux':
        cpu = '-j' + str(multiprocessing.cpu_count() * 2)

    try:
        subprocess.check_call(['cmake', '--build', SHADERC_BIN, '--config',
                            'Release', '--', cpu], stderr=subprocess.STDOUT,
                            shell=WINDOWS)
    except subprocess.CalledProcessError as e:
        # If CMake fails to build, we revert to attempt to use Vulkan SDK
        if not vulkan_sdk_fallback():
            raise e
        else:
            return


if __name__ == '__main__':
    build()
