# PyShaderc

Table of Contents
=================

  * [What is it ?](#what-is-it-)
  * [API](#api)
  * [Installation](#installation)
  * [How to use it](#how-to-use-it)
    * [Getting started](#getting-started)
    * [Include support](#include-support)
  * [How to update shaderc](#how-to-update-shaderc)
  * [Community](#community)
  * [Supported By](#supported-by)


## What is it ?

This module allow you to compile glsl to Spir-V in Python.
It leverages power of the great [shaderc](https://github.com/google/shaderc)
library to compile glsl.


## API

```python
def set_include_paths(paths):
    """Set include paths

    This function allows you to update the include paths.
    Include paths are used with #include <file>.

    Args:
        paths (list[str]): List of paths
    """

def compile_file_into_spirv(filepath, stage, optimization='size',
                            warnings_as_errors=False):
    """Compile shader file into Spir-V binary.

    This function uses shaderc to compile your glsl file code into Spir-V
    code.

    Args:
        filepath (str): Absolute path to your shader file
        stage (str): Pipeline stage in ['vert', 'tesc', 'tese', 'geom',
                     'frag', 'comp']
        optimization (str): 'zero' (no optimization) or 'size' (reduce size)
        warnings_as_errors (bool): Turn warnings into errors

    Returns:
        bytes: Compiled Spir-V binary.

    Raises:
        CompilationError: If compilation fails.
    """

def compile_into_spirv(raw, stage, filepath, language="glsl",
                       optimization='size', suppress_warnings=False,
                       warnings_as_errors=False):
    """Compile shader code into Spir-V binary.

    This function uses shaderc to compile your glsl or hlsl code into Spir-V
    code. You can refer to the shaderc documentation.

    Args:
        raw (bytes): glsl or hlsl code (bytes format, not str)
        stage (str): Pipeline stage in ['vert', 'tesc', 'tese', 'geom',
                     'frag', 'comp']
        filepath (str): Absolute path of the file (needed for #include)
        language (str): 'glsl' or 'hlsl'
        optimization (str): 'zero' (no optimization) or 'size' (reduce size)
        suppress_warnings (bool): True to suppress warnings
        warnings_as_errors (bool): Turn warnings into errors

    Returns:
        bytes: Compiled Spir-V binary.

    Raises:
        CompilationError: If compilation fails.
    """
```

## Installation

**Note (Linux): You need `cmake` and `make`**

**Note (Windows): You need `cmake` and [Visual C++ 2015 Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools)**

```python
pip install pyshaderc
```

Or if you want the latest version:

```python
git clone https://github.com/realitix/pyshaderc.git
cd pyshaderc
python setup.py build
python setup.py install
```


## How to use it

### Getting started

So simple !

```python
import pyshaderc
spirv = pyshaderc.compile_file_into_spirv('/tmp/myshader.vs.glsl', 'vert')
```

If you want more control, you can use the lower-level function
`compile_into_spirv`.

### Include support

Pyshaderc supports `#include` preprocessor thanks to shaderc.
There are two ways to use it:

**`#include "myfile"`**

Include file relatively, it's intuitive.

**`#include <myfile>`**

Like in C, you can include from a list of paths. To use this way to include,
you must call `set_include_paths` with a list of directories to search for
before compiling your glsl code.


## How to update shaderc

Download the last shaderc version on github, put the third party libs in it
and just zip it. Then update the build script with the new zip name.


## Community

You can checkout my blog, I speak about **PyShaderc**:
[Blog](https://realitix.github.io)

## Supported By

PyShaderc is supported by helpful 3rd parties via code contributions, test devices and so forth.
Make our supporters happy and visit their sites!

![linagora](https://www.linagora.com/sites/all/themes/tux/logo.png)

