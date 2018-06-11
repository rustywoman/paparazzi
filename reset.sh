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

# Clear Test Configuration Json
rm -rf report/assets/json/*_report.json
rm -rf report/assets/json/*_main.json
rm -rf report/assets/json/*_multi.json
rm -rf report/assets/json/*_scan.json
rm -rf report/assets/json/*_search.json

# Clear Case Report
rm -rf report/case/___*.html
