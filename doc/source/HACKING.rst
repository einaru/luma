****************
Luma Development
****************

.. Contents
.. ========
.. 1. Getting Started
.. 1.1. Libraries and tools
.. 1.2. Development tools
.. 2. Repository Structure
.. 2.1. The luma folder
.. 2.2. The resources folder
.. 2.3. The tools folder
.. 2.4. The doc folder
.. 3. Development
.. 3.1. Coding Style
.. 3.1.1. Source code header
.. 3.1.2. Source code footer
.. 3.2. Plugin development
.. 3.2.1. Available Luma plugins
.. 3.2.2. A skeleton plugin
.. 3.2.3. Settings support for plugins
.. 4. Internationalization
.. 4.1. Translating the application
.. 4.2. Dynamic Translation of the application
.. 5. Documentation
.. 5.1. Source code documentation
.. 5.2. User documentation
.. 6. Deployment
.. 7. The Luma Tool Chain
.. 7.1. The Luma resource compiler
.. 7.2. The Luma internationalization tool
.. 7.3. The Luma predeployment tool
.. 7.4. The Luma GPL header generator


1. Getting Started
==================
This document is intended for Luma developers. For install instructions see the
user documentation, either on the Luma website (http://luma.sf.net/) or see the
INSTALL_ file in the source distribution.


.. _INSTALL: ./INSTALL.html


1.1. Libraries and tools
------------------------
In order to start *hacking* on the Luma source, you will need to install a few
libraries and tools that Luma depends upon. The following python libraries is
required for Luma development:

- python_ >= 2.6 < 3
- python-ldap_ >= 2.3
- PyQt4_ >= 4.8

When you have these dependencies installed, you can proceed to get your hand on
the Luma sourcecode. git_ is used to as the revision control system for Luma,
and in order to get your hand on the source code, you will need to install it. 
Git is available for both *Linux*, *Mac OSX* and *Windows*, and can be 
downloaded from http://git-scm.com.

The Luma git_ repository is hosted on sourceforge_. To clone and create your own
branch you can run the following commands in your favorite shell::

    $ git clone http://luma.sf.net/repo/luma.git luma-devel
    $ cd luma-devel
    $ git fetch
    $ git checkout -b my-luma-feature develop


.. _python: http://www.python.org/
.. _python-ldap: http://python-ldap.org/
.. _PyQt4: http://www.riverbankcomputing.com/software/pyqt/download
.. _git: http://git-scm.com/
.. _sourceforge: http://sourceforge.net/


1.2. Development tools
----------------------
There exists a number of tools that can be helpful when developing python and 
PyQt4 code. We also have produced some tools spesific for the Luma development 
and deployment process `7. The Luma Tool Chain`_.

- `Qt4 Designer`_:
  This application is part of the Qt framework, which is helpful for creating
  Qt graphical interfaces. You can create the GUI design and use the PyQt4 tool
  ``pyuic4`` to generate python source code from it.

- `Qt4 Linguist`_: 
  This application is part of the Qt framework, and is used for the 
  internationalization process for the application.

If you plan on contributing documentation to the application you will need the
following tools:

- reStructuredText_:
  This is the markup language we use to write the user doumentation. You should
  also write your source code doc strings in this syntax. A number of programs
  is included in this tool, that enable us to generate teh documentation in
  various formats. One of these are the ``rst2man`` program, by which the
  *nroff* manual page is generated.
- Sphinx_:
  *Sphinx*, the Python documentation generator, is used to produce the html
  documentation for the application. It is used together with reStructuredText.


.. _Qt4 Designer: http://doc.trolltech.com/4.7/designer-manual.html
.. _Qt4 Linguist: http://doc.trolltech.com/4.7/linguist-manual.html
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org/


2. Repository structure
=======================
The first thing you should do after all libraries and tools are installed, is to
get familiar with the structure of the repository:

::

    .
    |-- bin
    |-- contrib
    |-- data
    |-- doc
    |-- luma
    |   |-- base
    |   |   |-- backend
    |   |   |-- gui
    |   |   |-- model
    |   |   `-- util
    |   |-- plugins
    |   `-- test
    |-- resources
    |   |-- forms
    |   |-- i18n
    |   `-- icons
    |-- setup
    `-- tools


2.1. The luma folder
--------------------
The *Luma source code files* is located in the ``luma`` folder. This is where
you should put all your Luma python modules. In the ``luma`` folder you will
find the following python packages:

- ``base``:
  Contains modules for the base application, and is divided into:

   * ``base.backend``:
     Contains all modules that handles the underlaying functionality is located
     here. As a rule off thumb *you should not place any python code with gui
     dependencies in this package*.
   * ``base.gui``:
     Contains all the GUI related modules, including the MainWindow and all the
     Dialogs used by the main aplication.
   * ``base.util``:
     Contains all utility modules, that both the main application and plugins
     can make use off.

- ``plugins``:
  All the plugins that is shipped with the base Luma application is located in
  their own subfolder here.

- ``test``:
  All test code is located here. If (when) you write your own unit-tests you 
  should put them in this location. Python modules in this folder is not 
  included when deploying Luma.


2.2. The resources folder
-------------------------
The *Luma resource files* is located in the ``resources`` folder. This folder is
divided into several sub-folders:

- ``forms``:
  Contains all the *UI* files created with the *Qt Designer* tool. All UI files
  should be placed here with a ``*Design.ui`` extension. Note that we mark these
  files with the *Design* suffix in order to easily distinguish them when python
  code is generated from them. Note also that *UI* files for plugins should be
  placed in its own subfolder under the ``plugins`` subfolder.

- ``i18n``:
  Contains all the translation files. When new translation files is created,
  they should be placed here, with a valid 2 char suffix, following the
  *ISO 638-1 standard* [1]_ and a ``.ts`` extension. Luma makes use of the Qt
  internazionallization system, and is translated with the Qt Linguist tool.
  Note that both the translation source files ``.ts`` and the release files 
  ``.qm`` should be placed in the same folder.

- ``icons``:
  Contains all the icons that is used by the application. The folder structure
  and icon naming should follow the icon-theme_ and icon-naming_ recommendations
  provided by the freedesktop.org_ project.


.. _icon-theme: http://www.freedesktop.org/wiki/Specifications/icon-theme-spec
.. _icon-naming: http://www.freedesktop.org/wiki/Specifications/icon-naming-spec
.. _freedesktop.org: http://www.freedesktop.org/wiki/


2.3. The tools folder
---------------------
The *Luma tool chain* is located in the ``tools`` folder. Here you find a number
of utility scripts that automates much of the postprocessing of resources for
the applications. See the section `7. The Luma Tool Chain`_ for a more detailed
description of what you find here.


2.4. The doc folder
-------------------
The Luma *User documentation files* is located in the ``doc`` folder. For 
information on how to contribute user documentation for Luma, please refer to
the `5.2. User documentation`_ section in this document.


3. Development
==============

3.1. Coding Style
-----------------
You should follow PEP8_ when writing Python source code for Luma. You should
especially try to use:

- 4 spaces for indentation
- CamelCase for methods name
- a maximum of 79 characters per line for code
- a miximum of 72 characters per line for docstrings
- one newline between class methods.
- two newlines between module methods.
- double underscore for *private* attributes and methods.
- python properties for getters and setter
- import statements as described in PEP328_

The *Coding Style* guidelines is **only guidelines**, meaning that the first
(and main) priority is allways to write **well documented** and **readable
code**. If these guidelines renders your implementation *less readable* or 
*less understandable*, you are free to (and should) bypass the affected 
guideline, and perhaps consider proposing modifications to the *Coding Style*
guidelines.


.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _PEP328: http://www.python.org/dev/peps/pep-0328/


3.1.1 Source code header
........................
When writing python modules for the Luma base application, you should include a
header comment that describes the name of the contributors and the license for 
the module. The contributors should be grouped by year. If you modify an 
existing module you can add your name and email to the contributor list (if you
feel you deserve it :) ).

Remember that the base Luma application is released under the *GNU General
Public License version 2* or newer. When you contribute new modules you should
also make them available under the same license. If you have some issues, i.e.
uses code that is made available under another license, you should consult the
Luma development theme. A list of GPL compatible licenses is available at:
http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses.

Belov is the default source code header used for the python modules in the base
Luma application::

    # -*- coding: utf-8 -*-
    #
    # package.module
    #
    # Copyright (c) <year>
    #      Your Name, <your@email.address>
    #
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 2 of the License, or
    # (at your option) any later version.
    #
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see http://www.gnu.org/licenses/


3.1.2. Source Code Footer
.........................
Because a lot of the Luma developers is using the brilliant vim_ text editor,
you should also include the following entry at the end of your python modules::

    # vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

This way we can eliminate some possible issues regarding mixing of tabs and
spaces.


.. _vim: http://vim.org/


3.2. Plugin development
-----------------------
Luma support plugins written in python and PyQt4, and most of the functionality
that Luma provides, comes through independent plugins. Most notably is the
*Browser* plugin that enables the user to browse an LDAP enabled server much
like a regular file browser.

Below are a selection of criterias that a Luma plugin *must* or *should* meet,
in order to be included in the base application.

- It *must* be written in python and PyQt4.
- It *must* be *cross-platform*, i.e. The plugin must provide the same 
  functionality on all supported platforms (*Linux*, *Windows* and *Mac OSX*).
- It *must* be available under the *GNU General Public License version 2* or
  newer, or another GPL compatible license [2]_.
- It *should* provide usefull LDAP related functionality.


3.2.1. Available Luma plugins
-----------------------------
The currently available plugins that is included in Luma is:

- *Browser*
- *Template*
- *Search*

Plugins that aws included in Luma 2.4, but is not yet ported to PyQt4 is:

- *Schemabrowser*
- *Massive User Creation*
- *User Management*
- *Admin Utilities*


3.2.2. A skeleton plugin
------------------------
The Luma ``PluginLoader`` expects to find some attributes and methods in the
rootlevel ``__init__.py`` file in the plugin location. As a minimum, this file
should include the following::



    from base.util.IconTheme import iconFromTheme    
    from MyPlugin import (MyPluginWidget, MyPluginSettingsWidget)

    lumaPlugin = True
    pluginName = u'plugin-name'
    pluginUserString = u'Plugin name'
    version = u'0.1'
    author = u'Your Name'
    description = u"""A short and consize description of the plugin."""


    def getIcon(iconPath = None):
        """Returns the plugin icon, which should be a PyQt4.QtGui.QIcon.
        """
        return iconFromTheme('theme-icon', 'fallback-icon')


    def getPluginWidget(parent):
        """Returns the main plugin widget.Typically a
        PyQt4.QtGui.QWidget instance.
        """
        return MyPluginWidget(parent)


    def getPluginSettingsWidget(parent):
        """Returns the settings widget for the plugin. Typically a
        PyQt4.QtGui.QWidget instance.
        """
        return MyPluginSettingsWidget(parent)


    def postprocess():
        return


3.2.3. Settings support for plugins
-----------------------------------
In the ``base.backend`` package of the Luma distribution, there is a settings
wrapper for plugins. This class give plugins aksess to the main application
configuration file. If you need to save some settings for your plugins you 
*must* implement a ``writeSettings`` method in the plugin settings widget::

    class MyPluginSettingsWidget(QWidget):
        """This class provides the GUI for editing the available settings
        for the `MyPlugin` plugin.
        """

        def loadSettings(self):
            """Loads the plugin settings using the PluginSettings class.
            """
            settings = PluginSettings('plugin-name')
            someValue = settings.pluginValue('some-key')

        def writeSettings(self):
            """Slot for the onSettingsChanged signal (emitted from the 
            SettingsDialog). Writes the plugin settings to disk.
            """
            settings = PluginSettings('plugin-name')
            settings.setPluginValue('some-key', 'some-value')
            del settings


4. Internationalization
=======================
One of the goals for Luma, in addition to create a supperior cross-platform LDAP
utility, is to provide the user with the ability to use Luma with the language
of his or her choosing. In order for this to be achieved we sorely depend on
translators from as amany countries as possible. In the following section we
describe a few conventions to follow when contributing translations to Luma.


4.1. Translating the application
--------------------------------
All translation files (both the source files (``.ts``) and the compiled files 
(``.qm``)) is located in the ``resources/i18n`` folder. To start translating
Luma to a new language you must create a suitable named ``.ts`` file. In order
for Luma to be able to correctly load the translation file you must choose a 
filename that conform to the Luma internationalization nameing convention.
Both ``luma_ll.ts`` and ``luma_ll_CC.ts`` is valid names, where ``ll`` is a two
letter lowercase ISO 639 language code [3]_, and ``CC`` is a two letter 
uppercase ISO 3266 country code [4]_. Note that the country code is not 
required. See section `7.2. The Luma internationalization tool`_ for a uility 
script that helps you pick the correct name for the translation target language.

.. todo::
    Describe how the empty ``.ts`` file is made ready for Qt4 Linguist

You must use `Qt4 Linguist`_ to write the actuall translation.

Finished translation source files (``.ts``) should be compiled into a (``.qm``))
file. Both files should be placed in the ``resources/i18n`` folder.


4.2. Dynamic Translation of the application
-------------------------------------------
In order to provide dynamic retransalation of the application at runtime a few
additional implementations must be added. This will be the same for all parts of
the application (both ``base`` and ``plugins``). The main concern is to make
sure the ``QEvent.LanguageChange`` [5]_ event is catched, and act accordigly 
upon it. It is recommended to create a dedicated method that can be called in 
order to offer the transalation of all the strings that should be translated::

    def changeEvent(self, event):
        """This event is generated when a new translator is loaded or the 
        system language (locale) is changed.
        """
        if QEvent.LanguageChange == event.type():
            self.retranslateUi(self)
            ...

    def retranslateUi(self):
        """Explicitly translate the gui strings."""
        self.someWidget.setText(QApplication.translate('some text'))
        ...

It is also possible to catch the ``QEvent.LanguageChange`` event with a event
handler implementation. You can look at the *Search* plugin for one possible
implementation of a dedicated event handler class.

Some aditional information on the internationalization support in the Qt4
framework and dynamic translation, can be found at
http://doc.trolltech.com/4.7/internationalization.html#dynamic-translation.


5. Documentation
================
Documentation is an essential part of open source projects, and you should
prioritice this when contributing to Luma.


5.1. Source code documentation
------------------------------
Python source code should allways be documented. First of all methods should
include a standard python docstring, describing the purpose of the method. 
Further more we belive that code can be written without the need for inline
comments. In some cases this is of course necessary and or desirable.

If you modify large blocks of code in a file, you might consider keeping the 
old codeblock in the file by commenting it out with the ``#`` character. You
should also add some information in relation to your new code, summarizing
the changes you have made.

When you document your source code, you should try to use reST_ style syntax,
in addition to following the before mentioned `3.1. Coding Style`_ guidelines.

Here is a mockup example of a class with reST_ style documentation::

    class Cosmik(object):
        """The `Cosmik` class mimics the myth and legend Frank Zappa.

        It includes some methods that does something and some methods that
        does other things.
        """

        def debris(self, paramOne, paramTwo):
            """Returns a list of cosmik debris given that some conditions
            is met. the empty list [] is returned if not.

            Parameters:

            - `paramOne`: this is used for some condition.
            - `paramTwo`: this is used to fetch debris.
            """
            cosmikDebris = []
            for x in self.__someInternalStuff(paramOne):
                if not someMagicalStuff(x, paramOne) is None:
                    cosmikDebris.append(self.someOtherStuff(x, paramTwo))
            
            return cosmikDebris


5.2. User documentation
-----------------------
The Luma *User documentation* files is located in the ``doc`` folder. We use 
reStructuredText (reSt_) and Sphinx_ to write and generate the documentation for
Luma. When you contribute new documentation files for Luma you should place the
documentation source files in the ``doc/source`` folder, and make sure the files
have a ``.rst`` extension. If you are unfamiliar with the reST_ syntax, please
refer to the `reStructuredText Primer`_ for a quickstart.

``Makefiles`` for both *UNIX* and *Windows* is available in the ``doc`` folder,
and in order to generate the html documentation you simple issue the following
commands from within the ``doc`` folder::

    $ cd doc
    $ sphinx-build source build

This will generate ``.html`` files from all the ``.rst`` files defined in the 
``index.rst``, located in the ``source`` folder, and put them in the ``build``
folder.


.. _reST: http://docutils.sourceforge.net/rst.html
.. _reStructuredText Primer: http://docutils.sourceforge.net/docs/user/rst/quickstart.html
.. _Sphinx: http://sphinx.pocoo.org/


6. Deployment
=============
Luma is currently deployed with `distutils_`, which is included in the python
standard library. The ``setup.py`` script is capable of creating source
distributions for *UNIX* and *Windows* systems, as well as binary distributions
for *Windows* (``.exe`` and ``.msi``) as well as generic ``.rpm`` packages, used
on a number of Linux systems.

All external resources that is to be included in the deployed application (such
as *icons*, *man pages*, *desktop entries*, etc) should be placed in the 
``data`` folder in the repository.

Example commands known to produce valid Luma distributions includes::

    $ python setup.py sdist        # -> tar.gz on UNIX, zip on Windows
    $ python setup.py bdist        # -> creates a dummy binary distribution
    $ python setup.py bdist_exe    # Windows
    $ python setup.py bdist_msi    # Windows
    $ python setup.py bdist_rpm    # Linux


.. _distutils: http://docs.python.org/distutils/


7. The Luma Tool Chain
======================
The ``tools`` folder in the repository contains the *Luma tool chain*, a 
selection of utility scripts that automates much of of the post processing of
resources, helps you getting started with Luma internationalization, etc.

The *Luma tool chain* currently contains:

- ``lumarcc.py`` - (see: `7.1. The Luma resource compiler`_)
- ``lumai18n.py`` - (see: `7.2. The Luma internationalization tool`_)
- ``lumadeploy.py`` - (see: `7.3. The Luma deployment preperation tool`_)

.. - ``luma-gplheader.py`` - (see: `7.4. The Luma GPL header generator`_)


7.1. The Luma resource compiler
-------------------------------
All the resource files located in the ``resources`` folder, described in section
`2.2. The resources folder`_, is processed in some way in order to make use of 
them in the running application. The ``lumarcc.py`` script can be used to update
both the resource file (``luma.qrc``), the project file (``luma.pro``), and the
translation files as well as generating python code from the *UI* files.
Translation files and icons are compiled into the a file named ``resources.py``
(located in the top-level source code folder). Python code for is generated from
the *UI* files, into locations based on the structure of the ``resources/forms``
folder.

For more information on how to use the ``lumarcc.py`` script, you can run it
with the ``-h`` or ``--help`` option::

    $ python lumarcc.py --help


7.2. The Luma internationalization tool
---------------------------------------
The ``lumai18n.py`` utility script helps new translators getting started with
new Luma translations. It is used to make sure that the name of the ``.ts``
file follows the conventions that is assumed by the rest of the aplication (see
section `4. Internationalization`_) The main concern is that the locale code 
choosen for a translation file, eventually becomes the alias used by the running
application when accessing the compiled version of this file.

For more information on how to use the ``lumai18n.py`` script, you can run it
with the ``-h`` or ``--help`` option::

    $ python lumai18n.py --help

.. note::
    The ``lumai18n.py`` script facilitates the ``PyQt4.QtCore.QLocale`` class. 
    The class reference can be viewed here 
    http://doc.trolltech.com/4.7/qlocale.html#name.


7.3. The Luma deployment preperation tool
-----------------------------------------
.. todo::
    Should first write this script :) and then possibly document it here.
    The idea behind the script is simple:
    It should be executed prior to genereating a release distribution of Luma,
    making sure that mainly the correct doc files is included in the root
    folder (INSTALL, HACKING, etc)


.. 7.4. The Luma GPL header generator
.. ----------------------------------
.. The ``lumagplheader.py`` script can be used to generate a Luma styled GPL-ed
.. source code header that includes all the elements described in section 
.. `3.1.1. Source code header`_. This script is also able to generate the vim-macro
.. footer, described in section `3.1.2. Source code footer`_
.. 
.. For more information on how to use the ``lumagplheader.py`` script, you can run
.. it with the ``-h`` or ``--help`` option::
.. 
..     $ python lumagplheader.py --help



Footnotes
=========
.. [1] http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
.. [2] http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses.
.. [3] http://www.gnu.org/software/gettext/manual/gettext.html#Language-Codes
.. [4] http://www.gnu.org/software/gettext/manual/gettext.html#Country-Codes
.. [5] http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qevent.html#Type-enum

