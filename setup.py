from distutils.core import setup

setup(name='PyTangle',
      version='0.0.1',
      py_modules=['PyTangle'],
      author = 'Michael Scholtens',
      author_email = 'author.mscholtens@gmail.com',
      download_url = 'https://github.com/michaelscholtens/PyTangle',
      description = 'Python wrapper for the Crowdtangle API that returns results as pandas dataframes.',
      install_requires = ['pandas', 'numpy', 'requests', 'time', 'logging', 'collections', 'datetime']
      )