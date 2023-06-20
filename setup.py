import os
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# list of requirements for core packages
requirements = []
with open(os.path.join(HERE, "requirements/requirements.txt"), "r") as fh:
    for line in fh:
        if not line.startswith("#"):
            requirements.append(line.strip())

# list of requirements for core packages
requirements_dev = []
with open(os.path.join(HERE, "requirements/requirements_dev.txt"), "r") as fh:
    for line in fh:
        if not line.startswith("#"):
            requirements_dev.append(line.strip())


setup(
    name="tau-slurm",
    version="0.0",
    url="https://github.com/SagiPolaczek/tau-slurm.git",
    author="Sagi Polaczek",
    author_email="sagi.polaczek@gmail.com",
    license="Apache License 2.0",
    description="Python utils for using TAU SLURM cluster",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
    },
)
