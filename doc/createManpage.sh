#!/usr/bin/env bash
#
# Utility script to create the luma nroff manpage from reST.
#
# 2011 Einar Uvsløkk <einar.uvslokk@linux.com>
#
# Needs the docutils program rst2man in order to work. 
# The script creates a standard .gz compressed manpage. To create a 
# manpage with a  different compression, just change the `gzip` 
# command. I.e. to  create a bz2 compression change it to bzip2.

# Change directory to the source folder
basepath=$(dirname $0)
cd $basepath/source

source_man="luma.1.rst"
target_man="luma.1"
location="../../data/man"

createManPage()
{
	echo "Running rst2man on $source_man"
	echo "Destination nroff manpage: $location"

	# The gzip of the man page is now handled during installation
	#rst2man $source_man > $location/$target_man ; gzip $location/$target_man
	rst2man $source_man > $location/$target_man
}

createManPage
