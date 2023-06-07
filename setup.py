import setuptools

VERSION = "1.1.2"
DESCRIPTION = "automates simple bettor tasks"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybettor",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ian-shepherd/pybettor",
    author="Ian Shepherd, Jason Lee, Jared Lee",
    author_email="ian.shepherd123@gmail.com, jason@aisportsfirm.com, 13jaredlee@gmail.com",
    install_requires=["numpy", "scipy", "matplotlib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
)
