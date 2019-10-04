#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    sys.exit('\nsetuptools is required')

params = {'entry_points': {'console_scripts': ['kanban = kanban:main']}}

setup(
    name='kanban',
    version='0.0.5',
    author='Luc Sinet',
    author_email='luc.sinet@gmail.com',
    description='Kanban application',
    long_description='A Kanban application in command line interface',
    long_description_content_type='text/markdown',
    url='https://github.com/Tastyep/Kanban',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    **params
 )
