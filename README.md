# pypge

[![Build Status](https://travis-ci.org/verdverm/pypge.svg)](https://travis-ci.org/verdverm/pypge)
[![PyPI](https://img.shields.io/pypi/v/pypge.svg)](https://pypi.python.org/pypi/pypge)
[![PyPI](https://img.shields.io/pypi/dm/pypge.svg)](https://pypi.python.org/pypi/pypge)


Python implementation of the [PGE algorithm](http://dl.acm.org/citation.cfm?id=2463486) 
(voted Best Paper Gecco 2013)

If you publish using this library, please cite the above paper.

PGE stands for Prioritized Grammar Enumeration and is *the* method for solving the Symbolic Regression problem. 

`This package is under heavy development until this comment is removed`


### Installation

You can install PyPGE with pip.

`pip install pypge`

#### Dependencies

PyPGE depends on several libraries, both Python and other.

Non-Python:

`apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran`

Python:

`pip install -r requirements.txt`

Alternatively you can use conda to install the Python dependencies:

`conda install --yes atlas numpy scipy pytest pandas scikit-learn sympy`

### scikit-learn integration

planned, of primary concern


### Things to know

* When pretty printing, sympy performs simplification, which can remove terms if the floating point print precision is not sufficient (looks like __zero__)


### Contributing

Branching practices follow the methodology outlined at: http://nvie.com/posts/a-successful-git-branching-model/


