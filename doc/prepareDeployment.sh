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

showHelp()
{
	echo "usage: $0 [options]"
	echo ""
	echo "$0 is used to ensure up-to-date doc files is included in the root"
	echo "folder prior to building a luma source distribution."
	echo ""
	echo "options:"
	echo ""
	echo "--h, --help  Display this help message."
	echo "--html       Also generate the html documentation." 
	echo "             This option requires sphinx to be installed"
	echo ""
	exit
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

case $1 in
	-h|--help)
		showHelp
		;;
	--html)
		copyDocFilesToRepoRoot
		generateHtmlDoc
		;;
	*)
		copyDocFilesToRepoRoot
		;;
esac

