"""Build with
   > py setup.py sdist"""

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    author = 'phantie',
    name = 'web_ext',
    version = '0.1',
    packages = find_packages()
)