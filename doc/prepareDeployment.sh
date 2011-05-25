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

