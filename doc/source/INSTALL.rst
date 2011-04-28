*******
INSTALL
*******
.. :Author: Einar Uvsløkk
   :Email:  einar.uvslokk@linux.com
   :Date:   April 14, 2011

Installing from the git repository
==================================
The Luma git_ repository is hosted on sourceforge_. To browse the repository
go to http://luma.sf.net/. You can install Luma from the repository if you
don't have an up to date packaged version or want to get the latest version 
from the trunk.

- Make sure you have git_ installed, you can check with::

	$ git --version

- Go to the directory you want to install Luma into and clone the repository::

	$ cd ~/bin
	$ git clone http://luma.sf.net/git/luma

After cloning the *Luma* repository you can now either `Run Luma from your local
copy`_, or do a `Systemwide install from your local copy`_.

.. _git: http://git-scm.org/
.. _sourceforge: http://sourceforge.net/


Run Luma from your local copy
-----------------------------
Create a symlink to the Luma startup script in a search ``PATH`` directory, for
example::

	$ ln -s ~/bin/luma-3.0.6/luma/luma.py ~/bin/luma

Systemwide install from your local copy
---------------------------------------
Use the ``setup.py`` file to install Luma using the python ``distutils``
module::

	$ sudo python setup.py install

NOTE: To uninstall you must manually delete all installed files. These are 
typically located in ``/usr/lib/python-xxx/site-packages/luma``

Source distribution installation
================================
Standard *python* source distribution is available for installation. If you 
are running *Linux* or another *UNIX-like system*, you can grab the latest 
source tarball, and `Install from tarball`_. If you are running *Microsoft 
Windows*, you can grab the latest zip-archive, and `Install from zip-archive`_.

Install from tarball
--------------------
If your *Linux* distribution does not have a `Prepackaged Luma distribution`_,
or if you prefer to install the latest Luma from source, download the latest 
tarball and install using the included ``setup.py`` script.::

	$ wget http://luma.sf.net/get/latest-tar
	$ tar xvzf luma-3.0.6.tar.gz
	$ cd luma-3.0.6
	$ sudo python setup.py install

Install from zip-archive
------------------------
If your installing on *Microsft Windows* you should download the zip-archive
from: http://luma.sf.net/get/latest-zip.::

	$ unzip luma-3.0.6.zip
	$ cd luma-3.0.6
	$ python.exe setup.py install

Prepackaged Luma distribution
=============================

.. note::
    This section just illustrated a proposed layout for *future* prepackaged 
    Luma distributions.

The following platform spesific Luma packages are available:

Linux
-----

**Fedora**::

	$ yum install luma

**Debian/Ubuntu**::

	$ apt-get install luma

**Arch**::

	$ pacman -S luma

Microsoft Windows
-----------------

An application bundle for *Microsoft Windows*, including all runtime 
dependencies can be downloaded from http://luma.sf.net/get/latest-win.

Mac OS X
--------

An application bundle for *Mac OS X*, including all runtime dependencies can
be downloaded from http://luma.sf.net/get/latest-mac.

