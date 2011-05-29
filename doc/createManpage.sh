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
#
# ----------------------------------------------------------------------
# This is a utility script to create the luma nroff manpage from reST.
# 
# It needs the docutils program rst2man in order to work.
# The script creates a standard .gz compressed manpage. To create a 
# manpage with a  different compression, just change the 'gzip'
# command. I.e. to  create a bz2 compression change it to bzip2.
# ----------------------------------------------------------------------

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
