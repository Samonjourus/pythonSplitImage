#!/usr/bin/env bash
mkdir empty
for a in $(ls | grep train);
 do
 rsync -a empty/ --delete $a
 rm -r $a
done
rm -r empty
