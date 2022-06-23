import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "LessAnnoyingPy",
    version = "1.0.0",
    author = "Nate Turner",
    author_email = "nathanturner270@gmail.com",
    description = ("Communicates to the Less Annoying CRM API using python."),
    url = "https://github.com/NathanTurner270/less-annoying-py",
    packages=find_packages(include=['LessAnnoyingPy', 'LessAnnoyingPy.*']),
    long_description=read('README.md'),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)
