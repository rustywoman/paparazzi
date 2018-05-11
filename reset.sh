#!/bin/sh
<<COMMENT
Reset
COMMENT

# Clear Log
rm -rf log/*

# Clear Cache
rm -rf ___cache/*

# Clear Screenshot
rm -rf ___screenshot/*

# Clear TMP
rm -rf ___tmp/*

# Clear Download Images
rm -rf report/assets/image/**

# Clear Style Result
rm -rf report/assets/json/**

# Clear Case Report
rm -rf report/case/___*.html
