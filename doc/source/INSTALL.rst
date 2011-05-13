*****************
Luma Installation
*****************

.. Contents
.. ========
.. 1. Platforms and dependencies
.. 2. Installing Luma from the git repository
.. 3. Installing Luma from a source distribution
.. 3.1. Installing the lateset tarball
.. 3.2. Installing the latest zipped archive
.. 4. Installing a prepackaged distribution of Luma
.. 4.1. Linux
.. 4.2. Microsoft Windows
.. 4.3. Mac OS X

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
- Chakra GNU/Linux: 2011.02 (Cyrus)
- Microsoft Windows: XP

In order to succesfully install and run Luma, you will need the to install the
following libraries on your syste on your systemm:

- Python >= 2.6 < 3
- python-ldap >= 2.3
- PyQt4 >= 4.8

You can install and/or run Luma in a number of ways. This includes:

.. - `2. Installing Luma from the git repository`_

- `2. Installing Luma from a source distribution`_
- `3. Installing a prepackaged distribution of Luma`_

.. This section is commented out because no real option is available for 
.. installing from git repository. Comment in again when this is available

.. 2. Installing Luma from the git repository
.. ==========================================
.. The Luma git_ reposotory is hosted on `SourceForge`_. To browse the repository
.. go to http://luma.cvs.sourceforge.net/viewvc/luma/. You can install or run Luma
.. from the repository if you don't have an up-to-date packaged version or want to
.. try the latest version.
.. 
.. First you need to make sure you have git_ installed, you can check with::
.. 
.. 	$ git --version
.. 
.. Go to the directory you want to install Luma into and clone the repository::
.. 
..     $ cd ~/bin 
..     $ git clone http://luma.sf.net/repo/luma.git luma
.. 
.. 
.. After cloning the Luma repository you are now able to run the application with
.. the following commands::
.. 
..     $ cd luma
..     $ python luma.py
..  
.. If you want to install Luma on your system, you can use the ``setup.py`` script
.. located in the repository root. This is a standard distutils style script, that
.. is invoked like this::
.. 
..     $ sudo python setup.py install
.. 
.. 
.. .. _git: http://git-scm.org/
.. .. _SourceForge: http://sourceforge.net/


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

**Fedora 14**

Testbuilds is currently available at http://folk.ntnu.no/einaru/luma/dist. 
To install run::

    $ wget http://folk.ntnu.no/einaru/luma/dist/luma-3.0.6b-4.fc14.noarch.rpm
    $ yum localinstall luma-3.0.6b-1.fc14.noarch.rpm --nogpgcheck


3.2. Microsoft Windows
----------------------
For Microsoft Windows there exists both ``.exe`` and  ``.msi`` installers. Note
that all the required dependencies must be installed seperately.

.. without the dependencies, as well as an application bundle that includs all 
.. necessary dependencies. These can be downloaded from the website
.. http://luma.sf.net/get/latest-win.


.. 4.3. Mac OS X
.. -------------
.. An application bundle for *Mac OS X*, including all runtime dependencies can
.. be downloaded from http://luma.sf.net/get/latest-mac.


