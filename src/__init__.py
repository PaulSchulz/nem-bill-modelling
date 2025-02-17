from setuptools import setup, find_packages

# Package name
PACKAGENAME = "nem_bill_modelling"

# Package version (replace with your package version)
VERSION = "0.1.0"

# Package description
DESCRIPTION = "A Python package for energy usage modelling and pricing."

# Long description (if applicable)
LONG_DESCRIPTION = """This package provides tools for modelling and analysing energy usage data."""
# Homepage URL (if available)
HOMEPAGE = "https://github.com/PaulSchulz/nem-bill-modelling"

# Author information
AUTHORS = """
Name: Paul Schulz
Email: paul@mawsonlakes.org
"""

# License information
LICENSE = "MIT"

# List of dependencies
DEPENDENCIES = [
    "pyyaml",
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    # Add any other Python packages your code depends on
]

# Scripts to run during installation (optional)
# scripts = {
#    "train": "train.py",  # Replace with the path to your main executable or script
# }

setup(
    name=PACKAGENAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Paul Schulz",
    author_email="paul@mawsonlakes.org",
    license=LICENSE,
    install_requires=DEPENDENCIES,
    scripts=scripts,
)
