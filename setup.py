#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'asyncio==3.4.3']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Adam Raźniewski",
    author_email='adam@razniewski.eu',
    python_requires='>=3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Get your active host list in N * timeout fixed time",
    entry_points={
        'console_scripts': [
            'asyncio_fast_portscanner=asyncio_fast_portscanner.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='asyncio_fast_portscanner',
    name='asyncio_fast_portscanner',
    packages=find_packages(include=['asyncio_fast_portscanner', 'asyncio_fast_portscanner.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Razikus/asyncio_fast_portscanner',
    version='0.0.1',
    zip_safe=False,
)
