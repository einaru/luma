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
Utility script for bumping the version of the Luma application.
Uses 'sed' to update the version variable in the version file.
The version string should be on the format:
 
    VERSION = 'version'

Where version typically is made up of version.release.modification,
i.e. 3.0.6.
"""
# The file(s) containing the version string
version_file="luma/__init__.py"
version_file_doc="doc/source/conf.py"
# The deployment script used to keep docfiles updated (html, dist)
deployment_script="doc/prepareDeployment.sh"

usage()
{
	cat <<-EndUsage
	Bump the version of Luma!
	
	usage: $0 [VERSION]
	
	If VERSION is missing you will be asked for the version.
	The new VERSION will be updated in two files:
	
	    $version_file
	    $version_file_doc

	NOTE: You must use a version number consisting of two or three
	dot-separated numeric components, as per the definitions found
	in the 'distutils.version.StrictVersion' module. See the module
	documentation for more information.

	The following are valid version numbers (shown in the order that
	would be obtained by sorting according to the supplied cmp function):
     
	    0.4       0.4.0  (these two are equivalent)
	    0.4.1
	    0.5a1
	    0.5b3
	    0.5
	    0.9.6
	    1.0
	    1.0.4a3
	    1.0.4b1
	    1.0.4
     
	The following are examples of invalid version numbers:
     
	    1
	    2.7.2.2
	    1.3.a4
	    1.3pl1
	    1.3c4
	
	NOTE: This script do not validate the VERSION number you provide.
	
	options:
	
	-h, --help   Prints usage and help.
	-d, --doc    Also generate the documentation files to reflect the
	             change of VERSION. This means running: 
	               
	EndUsage
}

ask_for_version()
{
	cat <<-EndAskForVersion
	Current version of Luma:
	  $(sed -n "/VERSION = '\(.*\)'/p" $version_file)
	Bump Luma to version: 
	EndAskForVersion

	read version
	bump_version $version
}

bump_version()
{
	echo -e "Bump version: $1 \n"

	sed -i "s/VERSION = '\(.*\)'/VERSION = '$1'/g" $version_file

	# For the shpinxdocumentation we operate with two version numbers,
	# `version` and `release`. Here `release` will contain possible
	# pre-relase tags (i.e. 'a', 'b', etc.) and will be the same as we
	# use for the $version_file. `version` in the doc configuration file
	# will be VERSION without the prelease tag.

	# `release`is the same as VERSION ($1).
	doc_release=$1
	# Look for pre-realse tags
	match=`echo $doc_release | egrep -o "[a-z].+?"`
	# `version` is `release` without pre-relase tags.
	doc_version=${doc_release/$match}

	sed -i "s/version = '\(.*\)'/version = '$doc_version'/g" $version_file_doc
	sed -i "s/release = '\(.*\)'/release = '$doc_release'/g" $version_file_doc
}

update_documentation()
{
	bash ./$deployment_script --all
}

if [[ "$1" == "" ]];
then
	ask_for_version
else
	case $1 in
		-h|--help) usage ;;
		-d|--doc)
			if [[ "$2" == "" ]];then
				ask_for_version
			else
				bump_version $2
			fi
			update_documentation ;;
		*)
			case $2 in
				-d|--doc) bump_version $1 ; update_documentation ;;
				*       ) bump_version $1 ;;
			esac
	esac
fi

exit 0
