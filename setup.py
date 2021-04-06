"""Build with
   > py setup.py sdist"""

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    author = 'phantie',
    name = 'fullmix',
    version = '0.2',
    packages = find_packages()
)