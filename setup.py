# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from dynamic_forms import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

standard_exclude = ["*.py", "*.pyc", "*~", ".*", "*.bak", "Makefile"]
standard_exclude_directories = [
    ".*", "CVS", "_darcs", "./build",
    "./dist", "EGG-INFO", "*.egg-info",
    "./example"
]

setup(
    name='dynamic-django-forms',
    version=__version__,
    description='JSON-Powered Dynamic Forms for Django',
    keywords='django,dynamic,forms,json',
    author='Alexander Skvortsov',
    author_email='sasha.skvortsov109@gmail.com',
    maintainer='Alexander Skvortsov',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=['django'],
    license='MIT License',
    packages=find_packages(exclude=['tests*', 'docs', 'example']),
    url='https://github.com/askvortsov1/dynamic-django-forms',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
