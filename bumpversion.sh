#!/usr/bin/env bash
#
# Copyright (c) Einar Uvsløkk 2011 <einar.uvslokk@linux.com>
#
# Utility script for bumping the version of the Luma application.
# Uses `sed` to update the version variable in the version file.
# The version string should be on the format:
#  
#     VERSION = 'version'
#
# Where version typically is made up of version.release.modification,
# i.e. 3.0.6.

# The file containing the version string
version_file="luma/__init__.py"

usage()
{
	cat <<-EndUsage
	Bump the version of Luma!
	
	usage: $0 [VERSION]
	
	If VERSION is missing you will be asked for the version.
	NOTE: There will be now validation on the version you choose
	
	options:
	
	-h, --help    Prints usage and help.

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
	sed -i  "s/VERSION = '\(.*\)'/VERSION = '$1'/g" $version_file
}

if [[ "$1" == "" ]];
then
	ask_for_version
else
	case $1 in
		-h|--help) usage ;;
		*        ) bump_version $1 ;;
	esac
fi

exit 0
