# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='FindPerfIssues',
    version='0.1.0',
    description='Find Performance Issues in Linux',
    long_description=readme,
    author='Koldo Oteo',
    author_email='koldo.oteo@gmail.com',
    url='https://github.com/SiteReliabilityEngineering/sre/tree/master/FindPerfIssues',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
