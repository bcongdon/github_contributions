#!/usr/bin/env python

from setuptools import setup

setup(name='GithubContributions',
      version='0.2.0',
      description='A Python interface for Github\'s user contribution system',
      author='Benjamin Congdon',
      author_email='me@bcon.gdn',
      url='https://github.com/bcongdon/github_contributions',
      packages=['github_contributions'],
      install_requires=[
          'requests',
          'bs4',
          'python-dateutil'
      ],
      extras_require={
          'dev': [
              'pytest',
              'responses==0.5.1',
              'mock'
          ]
      })
