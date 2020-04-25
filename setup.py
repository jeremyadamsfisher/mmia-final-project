#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name='MMIA Final Project Submission',
    author='Jeremy Fisher',
    packages=find_packages(),
    entry_points={"console_scripts": ['skeleregister = skeleregister.main:main']},
)