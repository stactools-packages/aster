# stactools-aster

[![PyPI](https://img.shields.io/pypi/v/stactools-aster)](https://pypi.org/project/stactools-aster/)

- Name: aster
- Package: `stactools.aster`
- [stactools-aster on PyPI](https://pypi.org/project/stactools-aster/)
- Owner: @gadomski
- [Dataset homepage](https://terra.nasa.gov/about/terra-instruments/aster)
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields: none
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/aster/main/examples/collection.json)

stactools package for working with ASTER data.

## STAC Examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation

```shell
pip install stactools-aster
```

## Command-line Usage

Description of the command line functions

```shell
stac aster create-item source destination
```

Use `stac aster --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest
```
