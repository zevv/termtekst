#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
import sys
import os


def check_requirements():
    assert os.geteuid() == 0, "Please run with root privileges."

try:
    check_requirements()
    setup(
    name = "termtekst",
    packages = find_packages(),
    version = "1.0.0",
    description = "NOS teletekst on the linux console",
    author = "Ico Doornekamp",
    author_email = "github@zevv.nl",
    url = "https://github.com/zevv/termtekst",
    keywords = ["teletekst", "terminal"],
    install_requires = ["requests"],
    classifiers = [],
    scripts=["src/tt"],
    include_package_data = True
    )
except AssertionError as e:
    print(e)
