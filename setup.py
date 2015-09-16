from distutils.core import setup
setup(
  name = 'pypge',
  packages = ['pypge'], # this must be the same as the name above
  version = '0.3',
  description = 'Prioritized Grammar Enumeration implementation',
  author = 'Tony Worm',
  author_email = 'verdverm@gmial.com',
  url = 'https://github.com/verdverm/pypge',
  keywords = ['pge', 'prioritized', 'grammar', 'enumeration', 'symbolic', 'regression', 'genetic programming'], # arbitrary keywords
  classifiers = [],
  install_requires=['sympy', 'pandas', 'lmfit'],
)