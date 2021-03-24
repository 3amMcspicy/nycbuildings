#!/usr/bin/env python3

"""
Install nycbulidings package
"""

from setuptools import setup


setup(
    name="nycbuildings",
    version="0.0.1",
    author="3amMcSpicy",
    author_email="",
    license="GPLv3",
    description="An interactive webapp to visualize electricity and water consumption data in NYCHA housing.",
    install_requires = ["pandas", "streamlit", "numpy", "pydeck"],
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={
        'console_scripts': []
    }
)    