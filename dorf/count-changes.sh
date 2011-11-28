#!/bin/bash

BASE=ubuntu910
OTHERS=`ls | grep -v __init__.py | grep -v "\.sh" | grep -v hashtable | grep -v $BASE`

for file in $OTHERS
do
	echo $BASE:$file
	diff -r $BASE/  $file/ | diffstat
	cloc hashtable/*.py $file/*.py ../*.py
	echo
done
