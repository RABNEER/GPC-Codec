from setuptools import setup, find_packages

setup(
    name="gpc-codec",
    version="1.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
