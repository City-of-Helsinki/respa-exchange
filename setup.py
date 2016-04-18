# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from respa_exchange import __version__

setup(
    name='respa-exchange',
    version=__version__,
    description='Bidirectional Microsoft Exchange synchronization for Respa',
    author='Aarni Koskela',
    author_email='aarni.koskela@andersinno.fi',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(include=['respa_exchange', 'respa_exchange.*']),
    include_package_data=True,
    install_requires=[l for l in open("requirements.txt", "rt").readlines() if l and not l.startswith("#")],
    zip_safe=False,
)
