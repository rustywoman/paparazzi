#!/bin/sh
<<COMMENT
Local Report Web Server
COMMENT

PORT=9191
HOST=127.0.0.1

echo
echo ----------------------------------------------------------
echo Start Report Server Process - http://${HOST}:${PORT}
echo ----------------------------------------------------------
echo

python -m http.server ${PORT}
