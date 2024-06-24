set -e

ECHO Test batch size = 10 with TMX sourced input
python main.py ../../test-resources/english-to-spanish.tmx.10.csv 10
