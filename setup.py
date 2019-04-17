#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
# syt
# Copyright (C) 2019  Markus Peröbner
#
from setuptools import setup
import os.path

setup(
    name='syt',
    version='0.2.0',
    license='AGPLv3',
    description='a tool for synchronizing things over removable media',
    author='Markus Peröbner',
    author_email='markus.peroebner@gmail.com',
    packages=[
        'syncthing',
    ],
    entry_points={
        'console_scripts': [
            'syt = syncthing.main:main',
        ],
    },
    data_files=[
        (os.path.join('share', 'doc', 'syt'), ['AUTHORS', 'LICENSE', 'README']),
    ],
    url='https://github.com/marook/syt',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
    ],
)
