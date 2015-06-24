# -*- coding: utf-8 -*-
#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()

packages = [
    'language_tags',
]

requires = ['six']

setup(
    name='language_tags',
    version='0.3.2',
    url='https://github.com/OnroerendErfgoed/language-tags',
    license='MIT',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    description='This project is a Python version of the language-tags Javascript project.',
    long_description=README + '\n\n' + HISTORY,
    zip_safe=False,
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License'
    ],
    platforms='any',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    test_suite='nose.collector'
)
