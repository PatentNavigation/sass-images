#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='sass-images',
    version='1.0',
    packages=find_packages(),
    url='',
    install_requires=['Pillow', 'six'],
    license='All rights reserved.',
    author='JOLT Labs',
    author_email='paul@joltlabs.com',
    description='',
    scripts=[
        'sass-images.py'
    ],
    test_suite="sass_images.tests"
)
