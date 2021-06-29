#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


with open(path.join(path.dirname(path.abspath(__file__)), "requirements.txt")) as requirement_file:
    requirements = requirement_file.read().split("/n")

setup_requirements = ["pytest-runner"]

with open(path.join(path.dirname(path.abspath(__file__)), "requirements-dev.txt")) as dev_requirement_file:
    test_requirements = dev_requirement_file.read().split("/n")

setup(
    author="Carlos Ávila",
    author_email='carlosavilacuevas13@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="opi_dragon_api",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords="opi_dragon_api",
    name="opi_dragon_api",
    packages=find_packages(include=['opi_dragon_api']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ceac33/opi-dragon-api',
    version='0.1.0',
    zip_safe=True
)
