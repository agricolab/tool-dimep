import setuptools
from distutils.core import setup
from pathlib import Path

# read the contents of README.md

this_directory = Path(__file__).parent
with (this_directory / "readme.md").open(encoding="utf-8") as f:
    long_description = f.read()

with (this_directory / "requirements.txt").open() as f:
    install_requires = f.readlines()

version = "0.3.1"


print(version)
setup(
    name="dimep",
    version="v" + version,
    description="Measures ipsilateral MEPs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    author="Robert Guggenberger",
    author_email="robert.guggenberger@uni-tuebingen.de",
    url="https://github.com/translationalneurosurgery/tool-dimep",
    download_url="git@github.com:translationalneurosurgery/tool-dimep.git",
    license="MIT",
    packages=setuptools.find_packages(exclude=["test", "docs"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
