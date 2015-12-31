__author__ = 'kronenthaler'

from setuptools import setup, find_packages


setup(name='SwiftFormat',
    author='Ignacio Calderon',
    description='A Swift parser and formatter',
    url="http://github.com/kronenthaler/swift-format",
    version='1.3',
    license='BSD License',
    packages=find_packages(exclude=['tests']))