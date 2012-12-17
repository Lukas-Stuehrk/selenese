# encoding: utf-8
import os
from setuptools import setup, find_packages
from selenese import __version__


here = os.path.abspath(os.path.dirname(__file__))


requires = ['lxml', 'selenium']


setup(name='selenese',
      version=__version__,
      description='A python library that reads selenese HTML files and makes them executable on a selenium webdriver object',
      classifiers=[
        "Programming Language :: Python"
        ],
      author='Lukas Stührk',
      author_email='Lukas@Stuehrk.net',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite='tests',
      tests_require=['selenium'],
      entry_points={
      }
)
