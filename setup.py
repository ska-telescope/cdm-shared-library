#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import setuptools

# prevent unnecessary installation of pytest-runner
needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []


with open('README.md') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='cdm-shared-library',
    version="1.0.0",
    description="Configuration data model library",
    long_description=readme + '\n\n',
    author="Hélder Ribeiro",
    author_email='helder.ribeiro@fc.up.pt',
    url='https://gitlab.com/ska-telescope/cdm-shared-library',
    packages=setuptools.find_namespace_packages(where='src', include=['ska.*']),
    package_dir={'': 'src'},
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    install_requires=[
        'astropy==4.0.1',
        'marshmallow>=3.0.0rc7',
    ],
    setup_requires=[] + pytest_runner,
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-forked',
        'pytest-json-report',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort']

    },
    dependency_links = [
        "https://pypy.org./project/astropy/"
    ]

)
