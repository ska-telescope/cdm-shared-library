#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='cdm-shared-library',
    version='0.0.9',
    description="Configuration data model library",
    long_description=readme + '\n\n',
    author="Hélder Ribeiro",
    author_email='helder.ribeiro@fc.up.pt',
    url='https://github.com/ska-telescope/cdm-shared-library',
    packages=[
        'cdm_lib',
    ],
    package_dir={'cdm-shared-library': 'cdm_lib'},
    include_package_data=True,
    license="BSD license",
    zip_safe=False,
    keywords='ska_cdm_shared_library',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    install_requires=['pytango'],  # FIXME: add your package's dependencies to this list
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-json-report',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort']
    }
)
