from PyQt4.QtCore import QSettings

settings = QSettings('luma', 'luma')
settings = QSettings('luma', QSettings.IniFormat)
print settings.fileName()