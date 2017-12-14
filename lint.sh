#!/bin/sh
<<COMMENT
Lint
COMMENT

pycodestyle python_modules/*.py --config=conf/pycodestyle.conf

pycodestyle python_modules/handler/*.py --config=conf/pycodestyle.conf
