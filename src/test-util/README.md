# test-util README

## Dependencies

- Python 3.11
- pyenv - if on Windows use [pyenv-win](https://github.com/pyenv-win/pyenv-win)

## Install

Switch to Python 3.11.6:

```
pyenv install 3.11.6
pyenv local 3.11.6
```

Setup a virtual environment:

```
python3 -m venv env

env\Scripts\activate
```

```shell
pip install -U cornsnake==0.0.26 iso639-lang==2.2.3
```

# tmx to CSV converter [tmx-to--test-data-csv.py]

## Example Usage

1. Download TMX file for English to Spanish from https://opus.nlpl.eu/GNOME/en&es/v1/GNOME

2. Save the file to the ../../temp folder.

2. Run the conversion tool

```shell
python tmx-to--test-data-csv.py ../../temp/en-es.tmx/en-es.tmx ../../test-resources/english-to-spanish.tmx.10.csv 10
```
