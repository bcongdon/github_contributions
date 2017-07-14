#!/usr/bin/env python

from distutils.core import setup

setup(name='GithubContributions',
      version='0.1',
      description='',
      author='Benjamin Congdon',
      author_email='me@bcon.gdn',
      url='https://github.com/bcongdon/github-contributions',
      packages=['github_contributions'],
      install_requires=[
        'requests',
        'bs4',
        'python-dateutil'
      ])
