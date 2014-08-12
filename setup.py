"""
Simple Secret App and Server
==============
"""
import sys

from setuptools import setup, find_packages

def get_requirements(suffix=''):
    with open('%srequirements.txt' % suffix) as f:
        rv = f.read().splitlines()
    return rv

def get_long_description():
    with open('README.md') as f:
        rv = f.read()
    return rv

setup(
    name='Simple Secret App',
    version='0.0.1',
    url='https://github.com/jamesonjlee/simple-secret-app',
    license='ARR',
    author='Jameson Lee',
    author_email='jamesonjlee@gmail.com',
    description='Simple Secret App Server and Client',
    long_description=get_long_description(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='osx',
    install_requires=get_requirements(),
    tests_require=get_requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
