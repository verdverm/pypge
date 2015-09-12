from distutils.core import setup
setup(
  name = 'pypge',
  packages = ['pypge'], # this must be the same as the name above
  version = '0.1',
  description = 'Prioritized Grammar Enumeration implementation',
  author = 'Tony Worm',
  author_email = 'verdverm@gmial.com',
  url = 'https://github.com/verdverm/pypge', # use the URL to the github repo
  download_url = 'https://github.com/verdverm/pypge/tarball/0.1', # I'll explain this in a second
  keywords = ['pge', 'prioritized', 'grammar', 'enumeration', 'symbolic', 'regression', 'genetic programming'], # arbitrary keywords
  classifiers = [],
  install_requires=['sympy', 'pandas', 'lmfit'],
)