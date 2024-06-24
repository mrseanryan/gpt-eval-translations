set -e

ECHO Test batch size = 10
python main.py ../../test-resources/english-to-spanish.csv 10
