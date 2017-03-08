from setuptools import setup, find_packages

setup(
    name="pyshaderc",
    version='1.0.6',  # can't use pyshader.__version__
    author="realitix",
    author_email="realitix@gmail.com",
    description="Python CFFI binding for shaderc",
    long_description="Python CFFI binding for shaderc",
    packages=['_cffi_build', 'pyshaderc'],
    install_requires=["cffi"],
    setup_requires=["cffi"],
    include_package_data=True,
    url="http://github.com/realitix/pyshaderc",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    license="Apache 2.0",
    ext_package="pyshaderc",
    cffi_modules=["_cffi_build/pyshaderc_build.py:ffi"]
)
