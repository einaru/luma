from PyQt4.QtGui import QWidget
from LoggerWidgetDesign import Ui_LoggerWidgetDesign

class LoggerWidget(QWidget, Ui_LoggerWidgetDesign):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setupUi(self)
        self.logList = []

    def clearLogger(self):
        self.logList = []
        self.messageEdit.clear()

    def rebuildLog(self):
        self.messageEdit.clear()
        for l in self.logList:
            loglvl, msg = l
            if loglvl == "DEBUG" and self.debugBox.isChecked():
                self.messageEdit.append("DEBUG: " + msg)
                continue
            if loglvl == "ERROR" and self.errorBox.isChecked():
                self.messageEdit.append("ERROR: " + msg)
                continue
            if loglvl == "INFO" and self.infoBox.isChecked():
                self.messageEdit.append("INFO: " + msg)
                continue


    def log(self, log):
        loglvl, msg = log
        if loglvl == "DEBUG" and self.debugBox.isChecked():
            self.logList.append(log)
            self.messageEdit.append("DEBUG: " + msg)
            return
        if loglvl == "ERROR" and self.errorBox.isChecked():
            self.logList.append(log)
            self.messageEdit.append("ERROR: " + msg)
            return
        if loglvl == "INFO" and self.infoBox.isChecked():
            self.logList.append(log)
            self.messageEdit.append("INFO: " + msg)
            return
        if loglvl not in ["INFO", "ERROR", "DEBUG"]:
            # This shouldn't really happen...
            # Please only use the above levels
            self.logList.append(log)
            self.messageEdit.append("UNKNOWN: " + msg)

