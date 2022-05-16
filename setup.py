import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybettor",
    version="1.0.0",
    author="Ian Shepherd, Jason Lee, Jared Lee",
    author_email="ian.shepherd123@gmail.com, jason@aisportsfirm.com, 13jaredlee@gmail.com",
    description="automates simple bettor tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ian-shepherd/pybettor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
