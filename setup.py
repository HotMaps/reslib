#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 16:24:17 2019

@author: ggaregnani
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="reslib",
    version="0.0.1",
    author='Giulia Garegnani',
    author_email='giuliagaregnani@gmail.com',
    description="Renewable energy plant classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HotMaps/reslib.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pandas', 'requests'
    ]
)
