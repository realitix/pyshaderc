from distutils.command.build import build
from setuptools import setup

from _cffi_build import shaderc_build


class ShadercBuild(build):
    def run(self):
        shaderc_build.build()
        super(ShadercBuild, self).run()


setup(
    name="pyshaderc",
    version='1.1.1',  # can't use pyshader.__version__
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
    cmdclass={'build': ShadercBuild},
    cffi_modules=["_cffi_build/pyshaderc_build.py:ffi"]
)
