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

# For SCSS
sass-lint 'front_end/scss/common/_base.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/common/_keyframes.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/common/_mixin.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/common/_reset.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/common/_settings.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/_top.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/_detail.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/_error.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_button.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_footer.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_header.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_loading.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_marker.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_overlay.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_tree.scss' -v -q --config .sass-lint.yml
sass-lint 'front_end/scss/page/part/_zoom.scss' -v -q --config .sass-lint.yml
# sass-lint 'front_end/scss/_highlight.scss' -v -q --config .sass-lint.yml
# sass-lint 'front_end/scss/_perfect_scroll.scss' -v -q --config .sass-lint.yml

# For Python
conf=conf/paparazzi.conf
pycodestyle python_modules/*.py --config=$conf --verbose --show-source --format '%(code)s: %(text)s' --benchmark
pycodestyle python_modules/handler/*.py --config=$conf --verbose --show-source --format '%(code)s: %(text)s' --benchmark
