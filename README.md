# organelle_transport_analysis
Package for running organelle transport analysis

Requires Python >=3.8

## Installation

Either use `.py` files from `/src/organelle_transport_analysis` directly or install as a local package.

To install as a package, run the following in this directory:

`python -m pip install -e .`

or

`python.exe -m pip install -e .`

This will install `organelle_transport_analysis` package, consisting of 4 modules:

- `kymographs`
- `directions`
- `velocities`
- `plotting`

## Usage

Importing:

`from organelle_transport_analysis import kymographs, directions, velocities, plotting`

Calling functions:

`kymos = kymographs.get_kymo("your_data.csv")`

For more information on usage and examples, please see [example/example.ipynb](/example/example.ipynb).

## Other

More information can be found on https://www.biorxiv.org/content/10.1101/2024.03.25.586639v2.abstract or contact me (Anna Gavrilova).