#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import TripMapR
version = TripMapR.__version__

setup(
    name='TripMapR',
    version=version,
    author="Rahul Verma",
    author_email='rahulv@gmail.com',
    packages=[
        'TripMapR',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.4',
    ],
    zip_safe=False,
    scripts=['TripMapR/manage.py'],
)
