# -*- coding: utf-8 -*-
#!/usr/bin/env python
from setuptools import setup, find_packages

requires = []

setup(
    name='language-tags',
    version='0.0',
    url='https://github.com/OnroerendErfgoed/language-tags',
    license='MIT',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    description='This project is a Python version of the language-tags Javascript project.',
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    platforms='any',
    packages=find_packages(),
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=requires
)
