import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="load-distributed-routing",
    version="1.0.5",
    license='MIT',
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kylebrain/networking-final-project",
    author="Kyle Brainard",
    author_email="kbrainard@nevada.unr.edu",

    packages=find_packages(include=['load_distributed', 'load_distributed.*']),

    install_requires=[
        "numpy"
    ],
    entry_points={"console_scripts": ["ldr=load_distributed.main:main"]},
)