"""
This project bridges PyXLL and Anvil applications.

It enables Excel add-ins to be written in Python using PyXLL, but for the Python code
to be executed remotely via Anvil.

For details about PyXLL, see https://www.pyxll.com, and for details about Anvil
see https://anvil.works.
"""
import setuptools

setuptools.setup(
    name="anvil-pyxll",
    version="0.1",
    author="PyXLL Ltd",
    author_email="info@pyxll.com",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "anvil-uplink"
    ]
)
