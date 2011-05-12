**************
Luma Userguide
**************

.. Contents
.. ========
.. 1. Getting started
.. 2. Editing the serverlist
.. 3. Managing plugins
.. 3.1. Activating a plugin
.. 3.2. Selecting and using a plugin
.. 4. Luma keyboard shortcuts
.. 5. Problems and bugs
.. 5.1. The Luma Logger Window
.. 5.2. Reporting bugs
.. 6. Contact and support

*Luma is LDAP management made easy.*

1. Getting started
==================
On UNIX and UNIX-like systems after a succesfull installation, Luma can be 
started from a shell, with the following command (provided the startup script
is installed in the system ``PATH``)::

    $ luma

On Windows systems you can start Luma from ``cmd.exe``. If you installed from
a source distribution this can be done with::

    $ luma.py

If you installed a frozen bundle of Luma, it can be started with::

    $ luma.exe

For an overview of the available commandline options, you can run::

    $ luma -h

If you are running on a UNIX or UNIX-like system, you can read the luma(1) man
page, by running::

    $ man luma(1)


2. Editing the serverlist
=========================
If you are running Luma for the first time you will be greeted with a *Welcome
Tab*. Here you will find a quick overview of how to get started using the Luma
application. The first thing you need to do is to edit the **serverlist**. This
can be done by selecting ``Edit → Server List`` from the menubar or with the 
keyboard shortcut ``Ctrl + Shift + S``.

When adding servers to the serverlist you are presented with alot of options.
The Server Dialog is basically divided into three section:

- **Network**:
  Here you can define the server hostname, port number and base DN to use.
- **Authentification**:
  Here you can choose how to bind to the server.
- **Security**:
  Here you can choose your connection type, server certificate and client
  certificate.


3. Activate and use a plugin
============================
When you have added servers to the serverlist its time to manage the available
plugins. By default no plugins is activated. To activate a plugin you must
select ``Edit → Settings`` from the menubar to open the settings dialog, and select the plugins tab. A list of all avilable
plugins will be shown, and you can select the plugins you can to activate.
If the plugin support it, you can also edit plugin spesific settings from the
same dialog.

When you have activated one or more plugins and closed the settings dialog, the
activated plugins will be listed in the *Plugins tab* in the main window. 
(If the *Plugins tab* is closed you can open it by selecting ``View → Show 
Plugin List`` from the menubar). To open a plugin you simply double click it, 
and a new tab will be created for the plugin. This way you can have multiple
plugins open at the same time.


3.1. Available plugins
----------------------
The base Luma application includes a number of plugins which brings and extends
functionality to the application. 
configure the plugin settings (if the plugin supports this).


3.1.1. Browser
..............
The browser consists of the list of server-trees on the left, and the entry-view on the right.

**Server tree**

The following operations is avaialable when rightclicking a node:
Edit server settings

- **Open**: Loads the selected object, if not already loaded, and displays it in the entry-view.
- **Reload**: Removes the children from memory, and reloads them.
- **Clear**: Remove the children from memory.
- **Set filter**: Set the search filter used to collect the children, and reloads them.
- **Set limit**: Set the limit of the nodes children.
- **Add**: Add an entry using the selected nodes DN, and the selected template.
- **Delete**: Delete the node on the server.
- **Export**: Export the entry to file, with subtree or with subtree and parent.


**Entry-view**

The entry-view has the following functionality (on top):

- **Reload**: Reload current entry, asks whether to save if it has been modified.
- **Save**: Save changes done to the current entry.
- **Add attribute**: Opens a dialog where you can select attributes from a list, and add them to the entry.
- **Delete object**: Deletes the entry from server, if it is a leaf node.
- **Switch between views**: A drop down list where you can select views.

And the following inside the document:

- **Delete objectclass**: A red cross behind the object class, deletes the object, and the attributes that are no longer supported.
- **Edit attribute (RDN)**: Add a attribute as RDN (only on CREATE).
- **Edit attribute (Password)**: Type a password, only ascii is allowed when using encryption.
- **Edit attribute (Binary)**: Edit a binary attribute, opens a file dialog.
- **Edit attribute (Normal)**: Plain text input (Not allowed for RDN).
- **Delete attribute**: Delete the attribute (Not allowed for must with only one value)
- **Export binary**: Export the value to file.


3.1.2 Templates
...............
- Description
- Figur


3.1.3. Search
.............
The search plugin supports arbritrary LDAP search operations on a selected 
server. The plugin also includes a convinient Filter builder, which can be used
to build complex LDAP search filters.


**Search form**

In the *Search form* you select the server you wish to do a search operation on,
the Base DN you wish to connect with, the search level, and a possible size
limit for the search. The search level options is:

- **SCOPE_BASE**:
- **SCOPE_ONELEVEL**:
- **SCOPE_SUBTREE**: (*Default*)

The *size limit* defines the maximum number of matches to retrive from the 
search operation. The default value is 0 (which is the same as None).

To perform a search you simply select a server, enter a search filter and click
on the *Search* button. If the search filter contains no syntax errors, a 
result view is displayed at the left. If the search filter contains syntax
errors, an error message is displayed. It is also possible to continue editing
the filter in the *Filter builder*, by clicking the tool button next to the 
Search button.


.. Add relevant screenshots of the Search plugin search form.


**Filter builder**

The *Filter builder* is intended to help the you construct complex LDAP search
filters. Based on the currently selected server you are presented with a
complete list of object classes and attributes that is supported on the server.

The *Filter builder* is divided into a search critaria component creator, and a
filter editor. When you create a search filter criteria, you insert it into the
editor. The component will be inserted at the cursor position in the editor.
In the filter editor you are able to perform various operations on selections.
This includes to ``or``, ``and`` or ``negate`` a selection of the search filter.
You also is able to insert escaped special characters into the filter.

Filters created in the *Filter builder* follows the *LDAP String Representation
of Search Filters* spesifications defined in ``RFC4514`` [1]_.


.. Add relevant screenshots of the Search plugin filter builder.


**Result view**

When a search operation successfully returns. The matching LDAP entries are
displayed in a new tab. The search result is displayed in a table view. The
collumns in this table represents the DN plus one column for every attribute
used in the search filter.

It is also possible to do additional filtering on columns in the result view.
To open the result view filter box you can use the keyboard shortcut ``Ctrl +
F``. Here you can choose the filtering sysntax to use and the column to apply
the filter on.

The available filter syntaxes is:

- **Fixed String**:
- **Regular Expression**:
  Note that this option can be very slow on large result sets.
- **Wildcard**:
  Note that this option can be very slow on large result sets.


.. Add relevant screenshots of the Search plugin result view.


4. Luma keyboard shortcuts
==========================

+-----------------------+-----------------------------------------------------+
| **Keyboard shortcut** | **Action**                                          |
+=======================+=====================================================+
| **Main Application**                                                        |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + L``          | Toggles the *Logger Window*                         |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + P``          | Show the *Plugin List*                              |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + Q``          | Quit the application                                |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + W``          | Close the currently selected tab                    |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + Shift + S``  | Open the Server dialog                              |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + Shift + W``  | Show the *Welcome Tab*                              |
+-----------------------+-----------------------------------------------------+
| ``F5``                | Reload the plugins                                  |
+-----------------------+-----------------------------------------------------+
| ``F11``               | Toggle fullscreen mode                              |
+-----------------------+-----------------------------------------------------+
| ``F12``               | Open the *About Dialog*                             |
+-----------------------+-----------------------------------------------------+
| **Search plugin**                                                           |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + F``          | Opens the filterbox in a result view                |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + W``          | Close the currently selected result view tab        |
+-----------------------+-----------------------------------------------------+
| **Browser plugin**                                                          |
+-----------------------+-----------------------------------------------------+
| ``Ctrl + W``          | Close the current entry tab                         |
+-----------------------+-----------------------------------------------------+

On Os X Ctrl is replaced with Meta


5. Problems and bugs
====================
Luma tries to provide relevant feedback to the user, when illegal operations, 
errors and/or other problems occure. If you encounter some issues where the
application feedback is missing, you can try to start the application from a
shell with the ``-v`` or ``--verbose`` option::

    $ luma --verbose

This will print more information, about what is going on, to *standard out*. It
is also possible to view *Error*, *Debug* and *Info* messages, produced by the
application, in `5.1. The Luma Logger Window`_.


5.1. The Luma Logger Window
---------------------------
The *Logger Window* is not displayed by default. To display it you can select
``View → Logger Window`` from the menu bar, or use the keyboard shortcut ``Ctrl
+ L``. If you want the *Logger Window* to be displayed everytime you start Luma
you can select this in the *Settings Dialog* (``Edit → Settings`` in the 
menubar).

The *Logger Window* can be customized to display only selected types of
messages. The message that Luma produces is categorized in:

- **Error**:
  Messages for things that have gone wrong.
- **Debug**:
  Messages mostly intended for the developers to hunt down various issues.
  Some of these messages can be of great value when a problem occurs.
- **Info**:
  Messages that only contain verbose information of things that happen
  succesfully.


5.2. Reporting bugs
-------------------
The Luma bugtracker can be found here: http://luma.sf.net/bugtracker.


6. Contact and support
======================
Application news and contact information can be found on the offical Luma 
website http://luma.sf.net/.


Footnotes
=========
.. [1] http://tools.ietf.org/html/rfc4515

