# pypge

Python implementation of the [PGE algorithm](http://dl.acm.org/citation.cfm?id=2463486) 
(voted Best Paper Gecco 2013)

PGE stands for Prioritized Grammar Enumeration and is *the* method for solving the Symbolic Regression problem. 

`This package is under heavy development until this comment is removed`

[![Build Status](https://travis-ci.org/verdverm/pypge.svg)](https://travis-ci.org/verdverm/pypge)

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

### Contributing

Branching practices follow the methodology outlined at: http://nvie.com/posts/a-successful-git-branching-model/


