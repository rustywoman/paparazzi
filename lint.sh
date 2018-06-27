#!/bin/sh
<<COMMENT
Lint
COMMENT

# For TypeScript
tslint -c tslint.json front_end/ts/main.ts
tslint -c tslint.json front_end/ts/libs.ts
tslint -c tslint.json front_end/ts/klass/MarkerHandler.ts
tslint -c tslint.json front_end/ts/klass/LoadingHandler.ts
tslint -c tslint.json front_end/ts/klass/DependencyTreeHandler.ts

# For Python
conf=conf/paparazzi.conf
pycodestyle python_modules/*.py --config=$conf --verbose --show-source --format '%(code)s: %(text)s' --benchmark
pycodestyle python_modules/handler/*.py --config=$conf --verbose --show-source --format '%(code)s: %(text)s' --benchmark
