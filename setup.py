# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='python-spore-codec',
    version='0.1.0',
    description='Spore codec for CoreAPI specification',
    long_description=readme,
    author='Arnaud Grausem',
    author_email='arnaud.grausem@gmail.com',
    url='https://github.com/unistra/python-spore-codec',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

