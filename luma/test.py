from PyQt4.QtCore import QCoreApplication, QThreadPool, QRunnable
import time, sys

class lol(QRunnable):
    def run(self):
	time.sleep(2)
	print "FERDIG :D:D"

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    for i in xrange(10):
	l = lol()
	QThreadPool.globalInstance().start(l)
    sys.exit(app.exec_())
