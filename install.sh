#!/bin/sh

ACT_DIR=`pwd`

cd components
for i in `ls -d *` ; do
	cd $i
	python ./setup.py install
	cd ..
done

