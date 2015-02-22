import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import version


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='sxsdiff',
    version=version.get_version(),

    description='Side by side diff generator for python',
    long_description=long_description,

    license='BSD',
    author='Timon Wong',
    author_email='timon86.wang@gmail.com',
    url='https://github.com/timonwong/sxsdiff',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    zip_safe=False,
    packages=find_packages(),
    install_requires=['diff-match-patch', 'six>=1.9.0'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
