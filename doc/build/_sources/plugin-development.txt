Luma Plugin Development
=======================

Luma is written in the **Python** programming language, and uses the **PyQt4** 
language bindings for the graphical user interface. Luma supports plugins 
written in **Python** and **PyQt4**.

Luma is developed with *python 2.7.x*, but should be compatible with the 
*pyhton 2.6.x* release aswell.

A Luma plugin must meet the following criterias to be included in the core
applications:

- It *must* be **cross-platform**: The plugin must provide the same 
  functionality on all supported platforms (Linux/Windows/Mac OSX).
- ...
- ...

Skeleton plugin
---------------
The Luma ``PluginLoader`` expects to find some attributes and methods in the
rootlevel ``__init__.py`` file in the plugin location. As a minimum, this file
should include the following::

    lumaPlugin = True
    pluginName = u'plugin-name'
    pluginUserString = u'Plugin name'
    version = u'0.1'
    author = u'Your Name'
    description = u"""A short and consize description of the plugin."""

    def getIcon(iconPath = None):
        """Returns the plugin icon, which should be a PyQt4.QtGui.QIcon.
        """
        return QtGui.QIcon('my-plugin-icon')


    def getPluginWidget(parent):
        """Returns the main plugin widget.Typically a
        PyQt4.QtGui.QWidget instance.
        """
        return MyPluginWidget(parent)


    def getPluginSettingsWidget(parent):
        """Returns the settings widget for the plugin. Typically a
        PyQt4.QtGui.QWidget instance.
        """
        return MyPluginSetingsWidget(parent)


    def postprocess():
        return

Writing and loading plugin-settings
-----------------------------------
In the ``base.backend`` package of the Luma distribution, there is a settings
wrapper for plugins. This class give plugins aksess to the main application
configuration file. If you need to save some settings for your plugins you 
*must* implement a ``writeSettings`` method in the plugin settings widget.::

    class MyPluginSettingsWidget(QWidget):

        ...

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

        ...

Internationalization Support for plugins
----------------------------------------
The Qt framework offers a good system for internationalization support. Luma
makes good use of this system in the core application. In order to provide
runtime retransalations of the plugin a few additional implementations must be
included for the plugin. 

- The plugin must catch the ``QEvent.LanguageChange`` [#qevent]_ event and act
  upon it. It is recommended to create a dedicated method that can be called in
  order to offer the transalation of the String values.

::

    def changeEvent(self, event):
        """This event is generated when a new translator is loaded or the 
        system language (locale) is changed.
        """
        if QEvent.LanguageChange == event.type():
            self.retranslateUi(self)
            ...

    def retranslateUi(self):
        """Explicitly translate the gui strings."""
        ...

It is also possible to catch the ``QEvent.LanguageChange`` event through a 
event handler implementation.

.. note:: 
   If you use ``QtDesigner`` to create the GUI files, the ``retranslateUi`` 
   method will be generated when running the ``pyuic4`` tool.


.. [#qevent] http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qevent.html#Type-enum
