from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get version file and read everything within.
about = {}
with open(path.join(here, "src", "__version__.py"), "r") as f:
    exec(f.read(), about)

# Get the long description from the readme file.
with open(path.join(here, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

# Get the dependencies from the packages.
with open(path.join(here, "packages", "dev.txt"), encoding="utf-8") as f:
    requires = [line for line in f if not line.startswith("--")]

setup(
    name=about["__package__"],
    author=about["__author__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    licence="MIT Open Licence.",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    keywords="markowitz modern portfolio optimization",
    packages=find_packages("src", exclude=["tests.*", "test*"]),
    install_requires=requires,
    package_dir={"": "src"},
)