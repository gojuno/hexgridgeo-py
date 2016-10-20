import os
import sys
from setuptools import setup

MIN_PYTHON = (2, 7)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write("Python {}.{} or later is required\n".format(*MIN_PYTHON))
    sys.exit(1)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='hexgridgeo-py',
    version='1.0.0',
    author='Andrew Kirilenko',
    author_email='iced@gojuno.com',
    maintainer='Alexander Verbitsky',
    maintainer_email='averbitsky@gojuno.com',
    description='HexGrid Geo',
    long_description=read('README.rst'),
    keywords='hexgridgeo',
    url='https://github.com/gojuno/hexgridgeo-py',
    py_modules=['hexgridgeo'],
    test_suite='test',
    install_requires=(
        'hexgrid-py==1.0',
    ),
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: BSD License',
    ],
)
