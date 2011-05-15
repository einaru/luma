#!/usr/bin/env bash
#
# Utility script for preparing a luma release.
#
# 2011 Einar Uvsløkk <einar.uvslokk@linux.com>
#
# The script is used to ensure up-to-date doc files is included in the
# root folder prior to building a luma source distribution.

# Change directory to the source folder
basepath=$(dirname $0)
cd $basepath/source

files_to_include=(AUTHORS ChangeLog HACKING INSTALL README)
location="../.."

for file in "${files_to_include[@]}";
do
	echo "Copying $file ..."
	cp $file.rst $location/$file
done

