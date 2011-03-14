
from PyQt4 import QtCore, QtGui
import luma_rc

class SplashScreen(QtGui.QSplashScreen):
    def __init__(self):
        QtGui.QSplashScreen.__init__(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u'splash_screen')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        splash_image = QtGui.QPixmap(u':/images/splash.png')
        self.setPixmap(splash_image)
        self.setMask(splash_image.mask())
        self.resize(128, 123)
        QtCore.QMetaObject.connectSlotsByName(self)

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName(_fromUtf8("SplashScreen"))
        SplashScreen.setWindowModality(QtCore.Qt.NonModal)
        SplashScreen.setEnabled(True)
        SplashScreen.resize(400, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SplashScreen.sizePolicy().hasHeightForWidth())
        SplashScreen.setSizePolicy(sizePolicy)
        SplashScreen.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(SplashScreen)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.SplashImage = QtGui.QLabel(SplashScreen)
        self.SplashImage.setText(_fromUtf8(""))
        self.SplashImage.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/splash.png")))
        self.SplashImage.setObjectName(_fromUtf8("SplashImage"))
        self.verticalLayout.addWidget(self.SplashImage)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QtGui.QApplication.translate("SplashScreen", "Splash Screen", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    lol = SplashScreen()
    lol.show()
    sys.exit(app.exec_())
    print "lol"
