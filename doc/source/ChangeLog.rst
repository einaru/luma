*********
ChangeLog
*********
.. This changelog will mainly contain changes made between different tags in
.. the master branch. Changes made in the devlopment branch is documented in
.. the git log.

3.0.6-2 (2011-05-16)
====================

- Fixed exception.ErrorType bug in LumaConnectionWrapper.

- Updated the error/exception feedback in the Search plugin

- Renamed the browser_plugin folder to browser

- Moved Plugin* related code out from the util package and into base.gui, 
  base.gui.design, base.model

- Fixed export subtree in Browser plugin.

3.0.6-1 (2011-05-15)
====================

- Some small fixes to the documentation files.

3.0.6 (2011-05-15)
==================
.. This marks the end of the project. Einar Uvsløkk <einar.uvslokk@linux.com>

- New Connection API introduced with the LumaConnectionWrapper. This includes
  wrapper methods (both sync and async) for the refactored LumaConnection.
  Uses signal and slots to notify results from the various operations.
  All Qt 4 dependencies is thus removed from the backend modules.

- Refactor cleanup of the menubar in the main window.

- Search plugin now supports none-ascii characters in both server name and 
  search filter strings.

- Dynamic translation implemented in the Template plugin.

- Improved (simplified) internationalization support

3.0.5-sprint5 (2011-04-11)
==========================
.. This marks the end of sprint 5. Einar Uvsløkk <einar.uvslokk@linux.com>

- Search plugin has got a few updates and improvements. The filter builder
  has replaced the old filter wizard, some UI fixes in the search form, and 
  the result view for displaying search results is implemented. New feature
  enabling additional filtering on returned search results.

- Template plugin improved with the option to define none required attributes
  to appear as required.


3.0.4-sprint4 (2011-03-25)
==========================
.. This marks the end of sprint 4. Einar Uvsløkk <einar.uvslokk@linux.com>
	
- Main-application: Support for commandline arguments added. As of now this
  includes mostly clear flags, to wipe clean malicious config settings.

- Browser-plugin: Added multiselection item export and delete. Lots of 
  improvments in the Browsers entry view, including basic support for different
  html layouts for the view.

- Template-plugin: Gui finished, logic on its way.

- Search-plugin: Skeleton gui, and basic functionality implemented.


3.0.3-sprint3 (2011-03-14)
==========================
.. This marks the end of sprint 3. Einar Uvsløkk <einar.uvslokk@linux.com>

- Luma is now able to load plugins from the default plugin location.

- The Browser plugin now supports editing entries

- A simple installation procedure is included, making use of pythons own 
  distutils module.


3.0.2-sprint2 (2011-03-01)
==========================
.. This marks the end of sprint 2. Einar Uvsløkk <einar.uvslokk@linux.com>

- Plugin support is partly implemented. Loading plugins is working, but no 
  *real* plugins is present at runtime yet.

- The Browser plugin is partly implemented, but not integrated into the
  application yet.

- An extended QSettings class is implemented, with transparent support for 
  loading and saving application  settings. Settings is loaded and saved from 
  both the main window and the newly implemented settings dialog.

- Full translation is available for English and Norwegian, and can be changed,
  from both the settings dialog and the application menu bar, at runtime 
  without changing the application state.


3.0.1-sprint1 (2011-02-28)
==========================
.. This marks the end of sprint 1. *Einar Uvsløkk* <einar.uvslokk@linux.com>

.. note::
   This relase branch was tagged and created at the end of sprint 2, but still
   reflects the work done up until the end of sprint 1. It was created to 
   document the development progression.

- The Menu bar is restructured compared to Luma 2.4, various platforms *Human
  Interface Guidelines*.

- The Plugin toolbar is implemented, but with no real functionality yet.

- The Logger Window is implemented and displayes various logging levels, using
  the builtin python logging module.

- About dialog is implemented, and completely rewritten compared to Luma 2.4,
  inspired by gtk and gnome.

- The Server dialog GUI is implemented. Support for reading and saving the 
  server list is also implemented.

- Translation files is loaded dynamically. Uses the old translation files, 
  which still works on parts of the application. The languages can be selected
  from the menu bar, which is populated dynamically on startup.

