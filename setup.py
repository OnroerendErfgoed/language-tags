# -*- coding: utf-8 -*-
#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

packages = [
    'language_tags',
]

requires = ['pytest',
            'pytest-cov']

setup(
    name='language_tags',
    version='0.0',
    url='https://github.com/OnroerendErfgoed/language-tags',
    license='MIT',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    description='This project is a Python version of the language-tags Javascript project.',
    tolong_description=README,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    platforms='any',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    test_suite='nose.collector'
)
