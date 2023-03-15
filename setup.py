# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))
README = open(os.path.join(HERE, "README.md")).read()
REQUIREMENTS = open(os.path.join(HERE, "requirements.txt")).readlines()


setup(
    name="skatepedia-api",
    version="0.1.0",
    description="Skatepedia API",
    long_description=README,
    author="miguelgr",
    author_email="miguelgr@fastmail.com",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=["Internal :: Do not upload", "Programming Language :: Python :: 3"],
)
