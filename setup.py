#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name='MMIA Final Project Submission',
    author='Jeremy Fisher',
    packages=find_packages(),
    entry_points={"console_scripts": ['skeleregister = skeleregister.main:main']},
    include_package_data=True,
    package_data={"templates": [
        "UAB006-RF.jpg",
        "UAB007-LF.jpg",
        "UAB012-LH.jpg",
        "UAB013-RH.jpg",
    ]},
    zip_safe=True,
)