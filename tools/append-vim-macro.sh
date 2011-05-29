#!/bin/bash
# 
# append-vim-macro.sh
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

vimMacro="# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4"
root="luma"

usage()
{
	cat <<-EndUsage
	Usage: $0

	$0 scans through the $root source folder, to see if the	vim macro:
	 
		$vimMacro
	 
	is present at the end of each python module. If it's not the macro
	will be ppended to the module. The script should takes no arguments. 
	EndUsage
}

case $1 in
    -h|--help) usage ; exit 0 ;;
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

