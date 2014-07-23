#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    'Flask',
    'python-magic',
]

entry_points = {
    'console_scripts': [
        'upload_processor = upload_processor:main',
        'ensure_dirs = upload_processor:ensure_dirs',
    ]
}

setup(
    name="upload_processor",
    version="0.0.1",
    license='MIT',
    description="upload_processor",
    author='proton',
    packages=[],
    install_requires=install_requires,
    entry_points=entry_points,
)
