#!/bin/sh
<<COMMENT
Lint
COMMENT

conf=conf/paparazzi.conf

pycodestyle python_modules/*.py --config=$conf --verbose --show-source --format '%(code)s: %(text)s' --benchmark

pycodestyle python_modules/handler/*.py --config=$conf --verbose --show-source --format '%(code)s: %(text)s' --benchmark
