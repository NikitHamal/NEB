#!/bin/bash
set -e
cd /tmp/h/nc; cat head.py $(ls u?.py 2>/dev/null) tail.py > /tmp/NEB/nursing/tools/check_nc.py
