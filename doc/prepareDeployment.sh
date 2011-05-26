#!/usr/bin/env bash
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
""" 
Utility script for preparing a luma release.

The script is used to ensure up-to-date doc files is included in the
root folder prior to building a luma source distribution.
"""
# Change directory to the source folder
basepath=$(dirname $0)
cd $basepath/source

files_to_include=(AUTHORS ChangeLog HACKING INSTALL README)
location="../.."

showHelp()
{
	cat <<-EndHelp
	usage: $0 [options]
	
	$0 is used to ensure up-to-date doc files is included in the root
	folder prior to building a luma source distribution.
	
	options:
	
	--h, --help  Display this help message.
	--update     Update the doc files, i.e. the defined files is copied 
	             into the repo root.
	--html       Generate the html documentation. This option requires
	             sphinx to be installed
	-a, --all    Update doc files and generate the html docs.
	
	EndHelp
}

noValidArgs()
{
	cat <<-EndNoArgs
	No valid arguments provided.
	Try runing $0 --help for more information.
	EndNoArgs
}

# Generate the html docs
generateHtmlDoc()
{
	cd ..
	sphinx-build -b html source build
	cd source
}

copyDocFilesToRepoRoot()
{
	for file in "${files_to_include[@]}";
	do
		echo "Copying $file ..."
		cp $file.rst $location/$file
	done
}

while true;
do
	case $1 in
		-h|--help) showHelp ; break ;;
		-a|--all ) copyDocFilesToRepoRoot ; generateHtmlDoc ; break ;;
		--update ) copyDocFilesToRepoRoot ; shift ;;
		--html   ) generateHtmlDoc ; shift ;;
		*        ) break ;;
	esac
done

