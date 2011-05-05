# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Skole\it2901\resources\forms\plugins\search\SearchPluginSettingsDesign.ui'
#
# Created: Thu May 05 14:02:42 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchPluginSettings(object):
    def setupUi(self, SearchPluginSettings):
        SearchPluginSettings.setObjectName(_fromUtf8("SearchPluginSettings"))
        SearchPluginSettings.resize(266, 168)
        self.gridLayout_2 = QtGui.QGridLayout(SearchPluginSettings)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.defaultsGroup = QtGui.QGroupBox(SearchPluginSettings)
        self.defaultsGroup.setObjectName(_fromUtf8("defaultsGroup"))
        self.gridLayout = QtGui.QGridLayout(self.defaultsGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scopeLabel = QtGui.QLabel(self.defaultsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeLabel.sizePolicy().hasHeightForWidth())
        self.scopeLabel.setSizePolicy(sizePolicy)
        self.scopeLabel.setObjectName(_fromUtf8("scopeLabel"))
        self.gridLayout.addWidget(self.scopeLabel, 2, 0, 1, 1)
        self.scopeBox = QtGui.QComboBox(self.defaultsGroup)
        self.scopeBox.setObjectName(_fromUtf8("scopeBox"))
        self.scopeBox.addItem(_fromUtf8(""))
        self.scopeBox.addItem(_fromUtf8(""))
        self.scopeBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.scopeBox, 2, 1, 1, 1)
        self.sizeLimitLabel = QtGui.QLabel(self.defaultsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizeLimitLabel.sizePolicy().hasHeightForWidth())
        self.sizeLimitLabel.setSizePolicy(sizePolicy)
        self.sizeLimitLabel.setObjectName(_fromUtf8("sizeLimitLabel"))
        self.gridLayout.addWidget(self.sizeLimitLabel, 3, 0, 1, 1)
        self.sizeLimitBox = QtGui.QSpinBox(self.defaultsGroup)
        self.sizeLimitBox.setMaximum(999999)
        self.sizeLimitBox.setObjectName(_fromUtf8("sizeLimitBox"))
        self.gridLayout.addWidget(self.sizeLimitBox, 3, 1, 1, 1)
        self.enableCompletionOpt = QtGui.QCheckBox(self.defaultsGroup)
        self.enableCompletionOpt.setEnabled(True)
        self.enableCompletionOpt.setChecked(False)
        self.enableCompletionOpt.setObjectName(_fromUtf8("enableCompletionOpt"))
        self.gridLayout.addWidget(self.enableCompletionOpt, 0, 0, 1, 2)
        self.enableHighlightingOpt = QtGui.QCheckBox(self.defaultsGroup)
        self.enableHighlightingOpt.setObjectName(_fromUtf8("enableHighlightingOpt"))
        self.gridLayout.addWidget(self.enableHighlightingOpt, 1, 0, 1, 2)
        self.gridLayout_2.addWidget(self.defaultsGroup, 0, 0, 1, 1)
        self.scopeLabel.setBuddy(self.scopeBox)
        self.sizeLimitLabel.setBuddy(self.sizeLimitBox)

        self.retranslateUi(SearchPluginSettings)
        self.scopeBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(SearchPluginSettings)
        SearchPluginSettings.setTabOrder(self.enableCompletionOpt, self.enableHighlightingOpt)
        SearchPluginSettings.setTabOrder(self.enableHighlightingOpt, self.scopeBox)
        SearchPluginSettings.setTabOrder(self.scopeBox, self.sizeLimitBox)

    def retranslateUi(self, SearchPluginSettings):
        SearchPluginSettings.setWindowTitle(QtGui.QApplication.translate("SearchPluginSettings", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultsGroup.setTitle(QtGui.QApplication.translate("SearchPluginSettings", "Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeLabel.setText(QtGui.QApplication.translate("SearchPluginSettings", "Search level:", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeBox.setItemText(0, QtGui.QApplication.translate("SearchPluginSettings", "SCOPE_BASE", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeBox.setItemText(1, QtGui.QApplication.translate("SearchPluginSettings", "SCOPE_ONELEVEL", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeBox.setItemText(2, QtGui.QApplication.translate("SearchPluginSettings", "SCOPE_SUBTREE", None, QtGui.QApplication.UnicodeUTF8))
        self.sizeLimitLabel.setText(QtGui.QApplication.translate("SearchPluginSettings", "Size limit", None, QtGui.QApplication.UnicodeUTF8))
        self.enableCompletionOpt.setText(QtGui.QApplication.translate("SearchPluginSettings", "Enable attribute autocompletion.", None, QtGui.QApplication.UnicodeUTF8))
        self.enableHighlightingOpt.setText(QtGui.QApplication.translate("SearchPluginSettings", "Enable filter syntax highlighting.", None, QtGui.QApplication.UnicodeUTF8))

