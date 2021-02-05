from setuptools import setup, find_packages

# read the contents of README file
from os import path
# get current file directory
this_directory = path.abspath(path.dirname(__file__))
# open README with UTF-8 encoding
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    # read README
    long_description = f.read()

setup(
      name='populate',
      version='0.0.1',
      description='populate db with random tables',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/abmamo/populate',
      author='Abenezer Mamo',
      author_email='contact@abmamo.com',
      license='MIT',
      packages=find_packages(exclude=("tests",)),
      include_package_data=True,
      install_requires=[
          # testing
          "pytest==6.2.2",
          "pytest-cov==2.11.1",
          # mock data generation
          "mock @ https://github.com/abmamo/mock/archive/v0.0.1.tar.gz",
          # mock db generation
          "fastdb @ https://github.com/abmamo/fastdb/archive/v0.0.1.tar.gz",
          # file 2 db extraction
          "fs2db @ https://github.com/abmamo/fs2db/archive/v0.0.1.tar.gz"
          ],
      zip_safe=False
)
