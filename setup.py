from setuptools import setup

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
      url='',
      author='Adam Michael Grbac',
      author_email='adam.grbac@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['sklearn','flask'],
      zip_safe=False)