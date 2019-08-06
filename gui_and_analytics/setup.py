# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='gui_and_analytics',
    version='0.1.0',
    description='GUI and Data analytics for capstone project',
    long_description=readme,
    author='Matthew Panzer',
    url='https://github.com/panzer/capstone-mppt',
    packages=find_packages(exclude=('__tests__'))
)
