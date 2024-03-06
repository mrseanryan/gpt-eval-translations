set -e

ECHO Test default - batch size = 1, detailed output
python main.py ../../test-resources/english-to-spanish.csv

ECHO Test batch size = 1
python main.py ../../test-resources/english-to-spanish.csv 1

ECHO Test batch size = 3
python main.py ../../test-resources/english-to-spanish.csv 3

ECHO Test batch size = 3 - MIXED languages
python main.py ../../test-resources/english-to-spanish-and-german.csv 3

ECHO Test batch size = 5 - MIXED languages
python main.py ../../test-resources/english-to-spanish-and-german.csv 5
