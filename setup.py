import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gateoverflow",  # Replace with your own username
    version="0.2.0",
    author="Vaibhav Mali",
    author_email="malivp3494@gmail.com",
    description="A command line interface for gate links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toxdes/opengate",
    install_requires=['tabulate',
                      'python-dateutil', 'requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
