from pyqtgraph.Qt import QtGui
from madulator import Madulator

app = QtGui.QApplication([])
mad = Madulator()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
