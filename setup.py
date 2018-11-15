#!/usr/bin/env python3

import setuptools
from mvg_console import __version__, __description__


# Long description
with open("README.md", "r") as f:
    long_description = f.read()
print(setuptools.find_packages())
setuptools.setup(
    name="mvg_console",
    version=__version__,
    description=__description__,
    long_description=long_description,
    author="Frank Lu, Aadhithya Sankar",
    url="https://github.com/frankzl/python_mvg_console_program.git",
    packages=setuptools.find_packages(),
    install_requires=['requests','colr','texttable','pprint'],
    entry_points={
        "console_scripts": ["mvg = mvg_console.get_info:main"]
    },  
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ]   
)
