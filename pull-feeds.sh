#!/bin/bash

# IFS=$"\x0D"
IFS=$'\n'$'\r'
c=0

rm feed-cache/*.xml
for f in `cat feeds.txt`;
do
	if [[ ${f:0:1} != "#" ]]
	then
		wget "$f" -O feed-cache/$c.xml
		c=`expr $c + 1`
	fi
done
