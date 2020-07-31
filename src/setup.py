import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aglaishealthchecker-stvoutsin", # Replace with your own username
    version="0.0.1",
    author="Stelios Voutsinas",
    author_email="stv@roe.ac.uk",
    description="Tool for Healtchecking Zeppelin and other Notebook Services",
    long_description="Tool for Healtchecking Zeppelin and other Notebook Services",
    long_description_content_type="text/markdown",
    url="https://github.com/stvoutsin/aglais-healthchecker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
