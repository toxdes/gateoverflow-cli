import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gateoverflow",  # Replace with your own username
    version="0.4.1",
    author="Vaibhav Mali",
    author_email="malivp3494@gmail.com",
    description="A command line interface for gateoverflow links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toxdes/opengate",
    install_requires=['tabulate',
                      'python-dateutil', 'requests', 'toml>=0.10'],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "gateoverflow=gateoverflow.opengate:start",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
