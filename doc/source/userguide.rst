.. Luma userguide
   Author: Einar Uvsløkk, <einar.uvslokk@linux.com>
   Date: April 17, 2011

*********
Userguide
*********

.. tip::
   For instruction on obtaining and installing Luma, see the INSTALL_ page.

.. _INSTALL: ./INSTALL.html

Starting Luma
=============

Provided a Python interpretter is installed on the system, and the startup 
script is located in the system ``PATH``, Luma can be started from a shell 
like this::

    $ luma

For an overview of the available commandline options, you can run::

    $ luma -h

If you are running on a UNIX or UNIX-like system, you can read the luma(1) man
page, by running::

    $ man luma.1

.. You can also read the `luma(1) manpage`__ online.

.. _manpage: luma.1.html

__ manpage_

Using Luma
==========

Luma is a cross-platform desktop application.

Luma base plugins
=================

The base Luma application includes a number of plugins which brings and extends
functionality to the application. By default all available plugins is enabled. 
To disable a plugin from loading on startup you can uncheck the desired plugin 
in the *settings dialog* ( ``menubar`` → ``edit`` → ``configure plugins`` ). 
In the same dialog you can also view _about_ information for the plugins, and 
configure the plugin settings (if the plugin supports this).

Browser
-------

- Description
- Figur

Templates
---------

- Description
- Figur

Search
------

The search plugin supports arbritrary LDAP search operations on a selected 
server. The plugin also includes a convinient *filter builder*, which can be
used to build complex LDAP search filters.

Search form
...........

- Description
- Figur

Filter builder
..............


- Description
- Figur

Result view
...........

- Description
- Figur

