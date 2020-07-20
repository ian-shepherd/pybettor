import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybettor",
    version="0.0.1",
    author="Ian Shepherd",
    author_email="ian.shepherd123@gmail.com",
    description="automates simple bettor tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/pybettor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)