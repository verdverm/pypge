from setuptools import setup, find_packages
setup(
  name = 'pypge',
  packages = find_packages(), # this must be the same as the name above
  version = '0.4',
  description = 'Prioritized Grammar Enumeration implementation',
  author = 'Tony Worm',
  author_email = 'verdverm@gmial.com',
  url = 'https://github.com/verdverm/pypge',
  keywords = ['pge', 'prioritized', 'grammar', 'enumeration', 'symbolic', 'regression', 'genetic programming'], # arbitrary keywords
  classifiers = [],
  install_requires=['sympy', 'numpy', 'lmfit', 'sklearn', 'deap', 'networkx'],
)