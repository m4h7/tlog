from setuptools import setup
import glob

setup(name='tlog',
      version='1.0',
      description='Trivial log',
      license='MIT',
      packages=['tlog'],
      py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
