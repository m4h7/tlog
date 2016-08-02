from setuptools import setup

setup(name='tlog',
      version='1.0',
      description='Trivial log',
      license='MIT',
      packages=['tlog'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
