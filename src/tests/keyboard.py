from pyqtgraph.Qt import QtCore
import pyqtgraph as pg


class KeyPressWindow(pg.GraphicsWindow):
    sigKeyPress = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, ev):
        self.scene().keyPressEvent(ev)
        self.sigKeyPress.emit(ev)


def key_pressed():
    print("Key pressed")


app = pg.mkQApp()
win = KeyPressWindow()
win.sigKeyPress.connect(key_pressed)
pl = win.addPlot()
pl.plot([x*x for x in range(-10, 11)])


app.exec_()
