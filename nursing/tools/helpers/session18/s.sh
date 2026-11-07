#!/bin/bash
# s.sh "query" ... : compact search (images only, top 5)
cd /tmp/NEB
for q in "$@"; do echo "## $q"; /tmp/v/bin/python nursing/tools/assetget.py search "$q" 2>&1 | grep -A1 "^FREE" | grep -v "^--" | paste - - | grep -iE "\.(jpe?g|png|svg|tiff?)[[:space:]]" | head -5 | sed -E 's/^FREE +File://; s/\t +/ | /' | cut -c1-150; done
