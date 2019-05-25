from pyqtgraph.Qt import QtGui, QtCore
from src.madulator import Madulator

app = QtGui.QApplication([])
mad = Madulator()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
