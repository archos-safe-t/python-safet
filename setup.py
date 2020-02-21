#!/usr/bin/env python3
import os
import subprocess

from setuptools import setup, Command
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install_scripts import install_scripts

install_requires = [
    'setuptools>=19.0',
    'ecdsa>=0.9',
    'mnemonic>=0.17',
    'requests>=2.4.0',
    'click>=6.2',
    "pyblake2>=0.9.3 ; python_version<'3.6'",
]

import sys
if '--disable-hidapi' in sys.argv:
    sys.argv.remove('--disable-hidapi')
else:
    install_requires.append('hidapi>=0.7.99.post20')

if '--disable-libusb' in sys.argv:
    sys.argv.remove('--disable-libusb')
else:
    install_requires.append('libusb1>=1.6.4')

from trezorlib import __version__ as VERSION


class RenameLib(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Rename the package name into "safetlib", and the commandline tool into "saftctl"
        subprocess.call(["A=trezorlib; B=safetlib; for i in $(grep -R $A -l --exclude-dir=.git ./build); do sed -i -e \"s/$A/$B/g\" $i; done"], shell=True)
        subprocess.call(["A=trezorctl; B=safetctl; for i in $(grep -R $A -l --exclude-dir=.git ./build); do sed -i -e \"s/$A/$B/g\" $i; done"], shell=True)
        subprocess.call(["rm -rf build/lib/safetlib"], shell=True)
        os.rename("build/lib/trezorlib", "build/lib/safetlib")


class RenameScript(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Rename the package name into "safetlib", and the commandline tool into "saftctl"
        subprocess.call(["A=trezorlib; B=safetlib; for i in $(grep -R $A -l --exclude-dir=.git ./build); do sed -i -e \"s/$A/$B/g\" $i; done"], shell=True)
        subprocess.call(["A=trezorctl; B=safetctl; for i in $(grep -R $A -l --exclude-dir=.git ./build); do sed -i -e \"s/$A/$B/g\" $i; done"], shell=True)


def _patch_rename_lib(cls):
    """Patch a setuptools command to depend on `rename_lib`"""
    orig_run = cls.run

    def new_run(self):
        orig_run(self)
        self.run_command('rename_lib')

    cls.run = new_run


def _patch_rename_script(cls):
    """Patch a setuptools command to depend on `rename_script`"""
    orig_run = cls.run

    def new_run(self):
        orig_run(self)
        self.run_command('rename_script')

    cls.run = new_run


_patch_rename_lib(build_py)
_patch_rename_lib(develop)
_patch_rename_script(install_scripts)


setup(
    name='safet',
    version=VERSION,
    author='Trezor - Archos',
    author_email='software@archos.com',
    description='Python library for communicating with the Archos Safe-T mini (Trezor compatible) Hardware Wallets',
    url='https://github.com/archos-safe-t/python-safet',
    packages=[
        'trezorlib',
        'trezorlib.messages',
        'trezorlib.qt',
        'trezorlib.tests.device_tests',
        'trezorlib.tests.unit_tests',
    ],
    scripts=['safetctl'],
    install_requires=install_requires,
    extras_require={
        'ethereum': [
            'rlp>=0.6.0',
        ],
    },
    python_requires='>=3.3',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass={
        'rename_lib': RenameLib,
        'rename_script': RenameScript,
    },
)
