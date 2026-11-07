#!/bin/bash
# pages.sh : build PDF, print page count and fails
cd /tmp/NEB; P=/tmp/v/bin/python
$P nursing/tools/nebpdf.py course/year-3/child-health-nursing 2>&1 | tail -4
