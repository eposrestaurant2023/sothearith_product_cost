from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sothearith/__init__.py
from sothearith import __version__ as version

setup(
	name="sothearith",
	version=version,
	description="Sothearith",
	author="Tes Pheakdey",
	author_email="pheakdey.micronet@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
