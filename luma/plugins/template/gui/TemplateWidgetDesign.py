# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Skole\it2901\resources\forms\plugins\template\TemplateWidgetDesign.ui'
#
# Created: Sun Mar 20 22:32:40 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TemplateWidget(object):
    def setupUi(self, TemplateWidget):
        TemplateWidget.setObjectName(_fromUtf8("TemplateWidget"))
        TemplateWidget.resize(700, 550)
        self.gridLayout_3 = QtGui.QGridLayout(TemplateWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter_2 = QtGui.QSplitter(TemplateWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBoxTemplates = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxTemplates.setObjectName(_fromUtf8("groupBoxTemplates"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBoxTemplates)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.pushButtonTemplatesSave = QtGui.QPushButton(self.groupBoxTemplates)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTemplatesSave.sizePolicy().hasHeightForWidth())
        self.pushButtonTemplatesSave.setSizePolicy(sizePolicy)
        self.pushButtonTemplatesSave.setObjectName(_fromUtf8("pushButtonTemplatesSave"))
        self.gridLayout_6.addWidget(self.pushButtonTemplatesSave, 1, 1, 1, 1)
        self.pushButtonTemplatesAdd = QtGui.QPushButton(self.groupBoxTemplates)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTemplatesAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonTemplatesAdd.setSizePolicy(sizePolicy)
        self.pushButtonTemplatesAdd.setObjectName(_fromUtf8("pushButtonTemplatesAdd"))
        self.gridLayout_6.addWidget(self.pushButtonTemplatesAdd, 1, 0, 1, 1)
        self.listViewTemplates = QtGui.QListView(self.groupBoxTemplates)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listViewTemplates.sizePolicy().hasHeightForWidth())
        self.listViewTemplates.setSizePolicy(sizePolicy)
        self.listViewTemplates.setObjectName(_fromUtf8("listViewTemplates"))
        self.gridLayout_6.addWidget(self.listViewTemplates, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 1, 2, 2, 1)
        self.pushButtonTemplatesDelete = QtGui.QPushButton(self.groupBoxTemplates)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTemplatesDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonTemplatesDelete.setSizePolicy(sizePolicy)
        self.pushButtonTemplatesDelete.setObjectName(_fromUtf8("pushButtonTemplatesDelete"))
        self.gridLayout_6.addWidget(self.pushButtonTemplatesDelete, 2, 0, 1, 1)
        self.pushButtonTemplatesDuplicate = QtGui.QPushButton(self.groupBoxTemplates)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTemplatesDuplicate.sizePolicy().hasHeightForWidth())
        self.pushButtonTemplatesDuplicate.setSizePolicy(sizePolicy)
        self.pushButtonTemplatesDuplicate.setObjectName(_fromUtf8("pushButtonTemplatesDuplicate"))
        self.gridLayout_6.addWidget(self.pushButtonTemplatesDuplicate, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBoxTemplates, 0, 0, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelServer = QtGui.QLabel(self.layoutWidget1)
        self.labelServer.setMinimumSize(QtCore.QSize(0, 20))
        self.labelServer.setObjectName(_fromUtf8("labelServer"))
        self.gridLayout_2.addWidget(self.labelServer, 0, 0, 1, 1)
        self.labelDescription = QtGui.QLabel(self.layoutWidget1)
        self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
        self.gridLayout_2.addWidget(self.labelDescription, 1, 0, 1, 1)
        self.lineEditDescription = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEditDescription.setObjectName(_fromUtf8("lineEditDescription"))
        self.gridLayout_2.addWidget(self.lineEditDescription, 1, 1, 1, 1)
        self.splitter = QtGui.QSplitter(self.layoutWidget1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.groupBoxObjectclasses = QtGui.QGroupBox(self.splitter)
        self.groupBoxObjectclasses.setObjectName(_fromUtf8("groupBoxObjectclasses"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBoxObjectclasses)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pushButtonObjectclassesAdd = QtGui.QPushButton(self.groupBoxObjectclasses)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonObjectclassesAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonObjectclassesAdd.setSizePolicy(sizePolicy)
        self.pushButtonObjectclassesAdd.setObjectName(_fromUtf8("pushButtonObjectclassesAdd"))
        self.gridLayout_5.addWidget(self.pushButtonObjectclassesAdd, 0, 1, 1, 1)
        self.listViewObjectclasses = QtGui.QListView(self.groupBoxObjectclasses)
        self.listViewObjectclasses.setObjectName(_fromUtf8("listViewObjectclasses"))
        self.gridLayout_5.addWidget(self.listViewObjectclasses, 0, 0, 3, 1)
        self.pushButtonObjectclassesDelete = QtGui.QPushButton(self.groupBoxObjectclasses)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonObjectclassesDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonObjectclassesDelete.setSizePolicy(sizePolicy)
        self.pushButtonObjectclassesDelete.setObjectName(_fromUtf8("pushButtonObjectclassesDelete"))
        self.gridLayout_5.addWidget(self.pushButtonObjectclassesDelete, 1, 1, 1, 1)
        self.groupBoxAttributes = QtGui.QGroupBox(self.splitter)
        self.groupBoxAttributes.setObjectName(_fromUtf8("groupBoxAttributes"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxAttributes)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tableViewAttributes = QtGui.QTableView(self.groupBoxAttributes)
        self.tableViewAttributes.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewAttributes.setObjectName(_fromUtf8("tableViewAttributes"))
        self.tableViewAttributes.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_4.addWidget(self.tableViewAttributes, 0, 0, 3, 2)
        self.pushButtonAttributesAdd = QtGui.QPushButton(self.groupBoxAttributes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAttributesAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonAttributesAdd.setSizePolicy(sizePolicy)
        self.pushButtonAttributesAdd.setObjectName(_fromUtf8("pushButtonAttributesAdd"))
        self.gridLayout_4.addWidget(self.pushButtonAttributesAdd, 0, 2, 1, 1)
        self.pushButtonAttributesDelete = QtGui.QPushButton(self.groupBoxAttributes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAttributesDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonAttributesDelete.setSizePolicy(sizePolicy)
        self.pushButtonAttributesDelete.setObjectName(_fromUtf8("pushButtonAttributesDelete"))
        self.gridLayout_4.addWidget(self.pushButtonAttributesDelete, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.splitter, 2, 0, 1, 2)
        self.labelServerName = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelServerName.sizePolicy().hasHeightForWidth())
        self.labelServerName.setSizePolicy(sizePolicy)
        self.labelServerName.setMinimumSize(QtCore.QSize(0, 20))
        self.labelServerName.setText(_fromUtf8(""))
        self.labelServerName.setObjectName(_fromUtf8("labelServerName"))
        self.gridLayout_2.addWidget(self.labelServerName, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(TemplateWidget)
        QtCore.QObject.connect(self.pushButtonAttributesAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.addAttribute)
        QtCore.QObject.connect(self.pushButtonObjectclassesAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.addObjectclass)
        QtCore.QObject.connect(self.pushButtonTemplatesAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.addTemplate)
        QtCore.QObject.connect(self.pushButtonAttributesDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.deleteAttribute)
        QtCore.QObject.connect(self.pushButtonObjectclassesDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.deleteObjectclass)
        QtCore.QObject.connect(self.pushButtonTemplatesDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.deleteTemplate)
        QtCore.QObject.connect(self.pushButtonTemplatesDuplicate, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.duplicateTemplate)
        QtCore.QObject.connect(self.pushButtonTemplatesSave, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateWidget.saveTemplate)
        QtCore.QMetaObject.connectSlotsByName(TemplateWidget)

    def retranslateUi(self, TemplateWidget):
        TemplateWidget.setWindowTitle(QtGui.QApplication.translate("TemplateWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxTemplates.setTitle(QtGui.QApplication.translate("TemplateWidget", "Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTemplatesSave.setText(QtGui.QApplication.translate("TemplateWidget", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTemplatesAdd.setText(QtGui.QApplication.translate("TemplateWidget", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTemplatesDelete.setText(QtGui.QApplication.translate("TemplateWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTemplatesDuplicate.setText(QtGui.QApplication.translate("TemplateWidget", "Duplicate", None, QtGui.QApplication.UnicodeUTF8))
        self.labelServer.setText(QtGui.QApplication.translate("TemplateWidget", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDescription.setText(QtGui.QApplication.translate("TemplateWidget", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxObjectclasses.setTitle(QtGui.QApplication.translate("TemplateWidget", "Objectclasses", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonObjectclassesAdd.setText(QtGui.QApplication.translate("TemplateWidget", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonObjectclassesDelete.setText(QtGui.QApplication.translate("TemplateWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxAttributes.setTitle(QtGui.QApplication.translate("TemplateWidget", "Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAttributesAdd.setText(QtGui.QApplication.translate("TemplateWidget", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAttributesDelete.setText(QtGui.QApplication.translate("TemplateWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))

