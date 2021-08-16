#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name='rpimonitor',
    version='0.1',
    packages=find_packages(include=['rpimonitor']),
    python_requires='>=3.6',
)
