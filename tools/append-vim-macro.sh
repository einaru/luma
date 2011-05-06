#!/bin/bash
# 
# append-vim-macro.sh
#
# Copyright (c) Einar Uvsløkk 2011 <einar.uvslokk@linux.com>

vimMacro="# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4"
root="luma"

help=""" \
$0 scans through the $root source folder, to see if the
vim macro
 
    $vimMacro ,
 
is present at the end of each python module. If it's not the macro will be 
appended to the module. The script should takes no arguments. 
"""

case $1 in
    -h|--help)
        echo  -e "$help"
        exit
        ;;
esac

if [[ `basename $0` == '.' ]];
then
    cd ..
else
    cd `dirname $0`
    cd ..
fi

for file in $(find $root \( -type f -a -name "*.py" -a ! -name "*Design.py" \));
do
	if [[ `tail -n 1 $file` != $vimMacro ]];
	then
		
		echo -e "\n$vimMacro" >> $file
	else
		echo "$file allready contains the vim macro"
	fi
done

