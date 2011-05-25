*****************
Luma Installation
*****************

.. Contents
.. ========
.. 1. Platforms and dependencies
.. 2. Installing Luma from a source distribution
.. 2.1. Installing the lateset tarball
.. 2.2. Installing the latest zipped archive
.. 3. Installing a prepackaged distribution of Luma
.. 3.1. Linux
.. 3.2. Microsoft Windows
.. 3.3. Mac OS X

1. Platforms and dependencies
=============================
Luma is a crossplatform application written in the Python programming language.
It is developed and continiously tested on a number of platforms and operating
systems. The development platforms include:

- Fedora: 14 (GNOME)
- Ubuntu: 10.04, 10.10
- Microsoft Windows: Vista, 7
- Mac OS X

In addition Luma is tested succesfully on the following platforms:

- Fedora: 14 (KDE)
- Fedora: 15 (GNOME 3)
- Chakra GNU/Linux: 2011.02 (Cyrus)
- Microsoft Windows: XP

In order to succesfully install and run Luma, you will need the to install the
following libraries on your syste on your systemm:

- Python >= 2.6 < 3
- python-ldap >= 2.3
- PyQt4 >= 4.8

You can install and/or run Luma in a number of ways. This includes:

- `2. Installing Luma from a source distribution`_
- `3. Installing a prepackaged distribution of Luma`_

2. Installing Luma from a source distribution
=============================================
Source distribution for Luma is avaliable for installation using the distutils
modules in the standard python library. Source distributions can be downloaded
as tarballs ``.tar.gz`` (UNIX and UNIX-like) or as zipped archives (Windows) 
``.zip``. If you are running on Linux you could see if your distribution provide
prepackaged distributions of Luma (`3. Installing a prepackaged distribution of
Luma`_)


2.1. Installing the latest tarball
----------------------------------
If you are installing on UNIX and UNIX-like systems, you should use the latest 
tarball. The tarballs is known to install without any problem on both Linux and
Mac OS X. Luma is easily installed with the following commands::

	$ tar xvzf luma-3.0.6.tar.gz
	$ cd luma-3.0.6
	$ sudo python setup.py install


2.2. Installing the latest zipped archive
-----------------------------------------
If you are installing on Microsft Windows you should download the latest zipped 
archive, and open your ``cmd.exe``::

	$ unzip luma-3.0.6.zip
	$ cd luma-3.0.6
	$ python.exe setup.py install


3. Installing a prepackaged distribution of Luma
================================================
The following platform spesific Luma packages are available:


3.1. Linux
----------

**Fedora 14+**

Testbuilds is currently available at http://folk.ntnu.no/einaru/luma/dist. 
To install run::


3.2. Microsoft Windows
----------------------
For Microsoft Windows there exists both ``.exe`` and  ``.msi`` installers. Note
that all the required dependencies must be installed seperately.

