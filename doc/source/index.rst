.. Luma documentation master file, created by
   sphinx-quickstart on Wed Apr 27 11:29:58 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Luma's documentation!
================================

Luma is an cross-platform and open soruce graphical utility for accessing and 
managing data stored on LDAP enabled servers. It is written in Python, using 
PyQt4 and python-ldap. Luma supports plugins through its own plugin system. A
selection of plugins is includeed in the base application, providing useful 
LDAP-functionality.

Plugins included in the base application:

- **Browser**: Provides a familiar interface to browse the entry tree on 
  connected LDAP enabled servers. Entry attributes can be edited and deleted.
  Supports adding filters to limit expansions on large subtrees.
- **Template**:
- **Search**: A specialized search plugin to do advanced and complex search on a
  LDAP server. Supports filter creation that can be applied in the Browser 
  plugin.
.. - **Schema browser**:
.. - **Addressbook**: 
.. - **Massive user creation**:
.. - **Admin utilities**:

Contents
--------

.. toctree::
   :maxdepth: 2

   README.rst
   INSTALL.rst
   userguide.rst
   development.rst
   plugin-development.rst
   ChangeLog.rst
   BUGS.rst
   AUTHORS.rst
   THANKS.rst

