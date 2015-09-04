from codecs import open
import os.path

from setuptools import (
    find_packages,
    setup,
)

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as fd:
    README = fd.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as fd:
    CHANGES = fd.read()

__version__ = '0.2'

setup(
    name='genc',
    version=__version__,
    description='Geopolitical Entities, Names and Codes (GENC)',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/hannosch/genc',
    author='Hanno Schlichting',
    author_email='hanno@hannosch.eu',
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    include_package_data=True,
    install_requires=[],
    keywords="country region codes names",
    packages=find_packages(),
    zip_safe=False,
)
