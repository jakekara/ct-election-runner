import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ct-election-runner", # Replace with your own username
    version="0.0.1",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    description="Library and CLI tool for downloading CT election data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakekara/ct-election-runner",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['ctrunner=ctrunner.cli.__main__:main'],
    },
    python_requires='>=3.6',
)