from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='redisext',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jason Baker',
      author_email='jason@apture.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'redis',
      ],
      tests_require=[
          'mock',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
