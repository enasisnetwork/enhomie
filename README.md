# Enasis Network Home Automator

Do not use this project, it is under active development!

Simplify deciding when to restore lights to their desired state.

[![](https://img.shields.io/github/actions/workflow/status/enasisnetwork/enhomie/build.yml?style=flat-square&label=GitHub%20actions)](https://github.com/enasisnetwork/enhomie/actions)<br>
[![codecov](https://codecov.io/gh/enasisnetwork/enhomie/graph/badge.svg?token=7PGOXKJU0E)](https://codecov.io/gh/enasisnetwork/enhomie)<br>
[![](https://img.shields.io/readthedocs/enhomie?style=flat-square&label=Read%20the%20Docs)](https://enhomie.readthedocs.io/en/stable)<br>
[![](https://img.shields.io/pypi/v/enhomie.svg?style=flat-square&label=PyPi%20version)](https://pypi.org/project/enhomie)<br>
[![](https://img.shields.io/pypi/dm/enhomie?style=flat-square&label=PyPi%20downloads)](https://pypi.org/project/enhomie)

## Future goals
- Validate configuration items like:
  - Device names in `desired`.
  - Scene names in `desired`.
  - Time period `start` and `stop` too far apart?
- Using the configuration, manage the Hue bridge (or other vendor).
  - Not everything, just lights, rooms, zones, and *maybe* scenes.
- Easy to use listener and ability to perform some basic actions.

## Installing the package
Installing stable from the PyPi repository
```
pip install enhomie
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/enhomie
```

## Documentation
Documentation is on [Read the Docs](https://enhomie.readthedocs.io).
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `docs/html` directory.

## Configuration example
Some basic configuration examples, more should be added.
- [Homie Groups](enhomie/homie/test/samples/groups.yml)
- [Homie Scenes](enhomie/homie/test/samples/scenes.yml)
- [Philips Hue Bridges](enhomie/philipshue/test/samples/bridges.yml)
- [Philips Hue Devices](enhomie/philipshue/test/samples/devices.yml)
- [Ubiquiti Routers](enhomie/ubiquiti/test/samples/routers.yml)
- [Ubiquiti Clients](enhomie/ubiquiti/test/samples/clients.yml)

## Additional scripts
- [dumper.py](dumper.py) is useful for dumping configuration.
- [scener.py](scener.py) is useful for setting scene on groups.

## Useful and related links
- https://ubntwiki.com/products/software/unifi-controller/api

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/enhomie.git
```
Set up the Python virtual environments expected by the Makefile.
```
make -s venv-create
```

### Execute the linters and tests
The comprehensive approach is to use the `check` recipe. This will stop on
any failure that is encountered.
```
make -s check
```
However you can run the linters in a non-blocking mode.
```
make -s linters-pass
```
And finally run the various tests to validate the code and produce coverage
information found in the `htmlcov` folder in the root of the project.
```
make -s pytest
```

## Build and upload to PyPi
Build the package.
```
make -s pypackage
```
Upload to the test PyPi.
```
make -s pypi-upload-test
```
Upload to the prod PyPi.
```
make -s pypi-upload-prod
```
