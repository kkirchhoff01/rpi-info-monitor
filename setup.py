#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name='rpimonitor',
    version='0.1.2',
    packages=find_packages(include=['rpimonitor']),
    install_requires=['requests'],
    python_requires='>=3.6',
)
