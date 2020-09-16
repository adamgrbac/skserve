from setuptools import setup
from setuptools import find_packages

with open("README.md","r") as fh:
	long_description = fh.read()

setup(name='skserve',
      version='0.1',
      description='Flask-derived wrapper to serve sklearn models',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
      ],
      url='https://github.com/adamgrbac/skserve',
      author='Adam Michael Grbac',
      author_email='adam.grbac@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['sklearn','flask','pandas'],
      test_suite="tests.test_all"
      zip_safe=False)