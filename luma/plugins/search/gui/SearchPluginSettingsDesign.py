# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/einar/Desktop/luma-release-tagging/resources/forms/plugins/search/SearchPluginSettingsDesign.ui'
#
# Created: Thu Mar 31 18:10:56 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SearchPluginSettings(object):
    def setupUi(self, SearchPluginSettings):
        SearchPluginSettings.setObjectName("SearchPluginSettings")
        SearchPluginSettings.resize(271, 168)
        self.gridLayout_2 = QtGui.QGridLayout(SearchPluginSettings)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.defaultsGroup = QtGui.QGroupBox(SearchPluginSettings)
        self.defaultsGroup.setObjectName("defaultsGroup")
        self.gridLayout = QtGui.QGridLayout(self.defaultsGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.enableCompletionOpt = QtGui.QRadioButton(self.defaultsGroup)
        self.enableCompletionOpt.setChecked(True)
        self.enableCompletionOpt.setObjectName("enableCompletionOpt")
        self.gridLayout.addWidget(self.enableCompletionOpt, 0, 0, 1, 2)
        self.scopeLabel = QtGui.QLabel(self.defaultsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeLabel.sizePolicy().hasHeightForWidth())
        self.scopeLabel.setSizePolicy(sizePolicy)
        self.scopeLabel.setObjectName("scopeLabel")
        self.gridLayout.addWidget(self.scopeLabel, 2, 0, 1, 1)
        self.scopeBox = QtGui.QComboBox(self.defaultsGroup)
        self.scopeBox.setObjectName("scopeBox")
        self.scopeBox.addItem("")
        self.scopeBox.addItem("")
        self.scopeBox.addItem("")
        self.gridLayout.addWidget(self.scopeBox, 2, 1, 1, 1)
        self.sizeLimitLabel = QtGui.QLabel(self.defaultsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizeLimitLabel.sizePolicy().hasHeightForWidth())
        self.sizeLimitLabel.setSizePolicy(sizePolicy)
        self.sizeLimitLabel.setObjectName("sizeLimitLabel")
        self.gridLayout.addWidget(self.sizeLimitLabel, 3, 0, 1, 1)
        self.sizeLimitBox = QtGui.QSpinBox(self.defaultsGroup)
        self.sizeLimitBox.setMaximum(999999)
        self.sizeLimitBox.setObjectName("sizeLimitBox")
        self.gridLayout.addWidget(self.sizeLimitBox, 3, 1, 1, 1)
        self.disableCompletionOpt = QtGui.QRadioButton(self.defaultsGroup)
        self.disableCompletionOpt.setObjectName("disableCompletionOpt")
        self.gridLayout.addWidget(self.disableCompletionOpt, 1, 0, 1, 2)
        self.gridLayout_2.addWidget(self.defaultsGroup, 0, 0, 1, 1)

        self.retranslateUi(SearchPluginSettings)
        self.scopeBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(SearchPluginSettings)

    def retranslateUi(self, SearchPluginSettings):
        SearchPluginSettings.setWindowTitle(QtGui.QApplication.translate("SearchPluginSettings", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultsGroup.setTitle(QtGui.QApplication.translate("SearchPluginSettings", "Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.enableCompletionOpt.setText(QtGui.QApplication.translate("SearchPluginSettings", "Enable attribute autocompletion.", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeLabel.setText(QtGui.QApplication.translate("SearchPluginSettings", "Search level:", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeBox.setItemText(0, QtGui.QApplication.translate("SearchPluginSettings", "SCOPE_BASE", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeBox.setItemText(1, QtGui.QApplication.translate("SearchPluginSettings", "SCOPE_ONELEVEL", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeBox.setItemText(2, QtGui.QApplication.translate("SearchPluginSettings", "SCOPE_SUBTREE", None, QtGui.QApplication.UnicodeUTF8))
        self.sizeLimitLabel.setText(QtGui.QApplication.translate("SearchPluginSettings", "Size limit", None, QtGui.QApplication.UnicodeUTF8))
        self.disableCompletionOpt.setText(QtGui.QApplication.translate("SearchPluginSettings", "Disable attribute autocompletion.", None, QtGui.QApplication.UnicodeUTF8))

