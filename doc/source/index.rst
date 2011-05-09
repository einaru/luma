.. Luma documentation master file, created by
   sphinx-quickstart on Wed Apr 27 11:29:58 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Luma's documentation!
================================
*Luma is LDAP management made easy!*

Luma is a cross-platform, open source LDAP browser and administration utility,
capable of managing data stored on LDAP enabled server. It is written in 
Python_, with PyQt4_ (*GUI*) and python-ldap_ (*LDAP connections*). Luma
supports plugins through its own plugin system. A selection of plugins, 
providing useful LDAP functionality, is includeed with the base application:

- **Browser**:
  Provides a familiar interface to browse the entry tree on connected LDAP 
  enabled servers. Entry attributes can be edited and deleted. Supports adding
  filters to limit expansions on large subtrees.
- **Template**:
- **Search**:
  A specialized search plugin to do advanced and complex search on a LDAP
  server. Supports filter creation that can be applied in the Browser plugin.

.. - **Schema browser**:
.. - **Addressbook**: 
.. - **Massive user creation**:
.. - **Admin utilities**:


.. _Python: http://python.org/
.. _PyQt4: http://www.riverbankcomputing.com/software/pyqt/download
.. _python-ldap: http://pyhton-ldap.org/

Contents
--------

.. toctree::
   :maxdepth: 2

   README.rst
   INSTALL.rst
   userguide.rst
   HACKING.rst
   lumaAPI.rst
   ChangeLog.rst
   BUGS.rst
   AUTHORS.rst
   THANKS.rst

