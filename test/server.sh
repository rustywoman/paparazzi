#!/bin/sh
<<COMMENT
Local Dummy Web Server
COMMENT

PORT=9999
HOST=127.0.0.1

echo
echo ----------------------------------------------------------
echo Start Test Server Process - http://${HOST}:${PORT}
echo ----------------------------------------------------------
echo

python -m http.server ${PORT}
