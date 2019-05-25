import numpy as np
import array
from src.generator import *
from src.spectogram import *
from PyQt5 import QtCore, QtGui

FREQUENCY = 11025
MAX_SAMPLES = 500000
CHUNK = 1024


class Samples:

    def __init__(self, signal: QtCore.pyqtSignal = None):
        self.expression = Generator(1).random_function()
        self.signal = signal
        self.samples = []
        self.position = 0

    def get_expression(self) -> Expression:
        return self.expression

    def set_expression(self, expression: Expression) -> None:
        self.expression = expression
        self.reset()

    def reset(self) -> None:
        self.position = 0
        self.samples.clear()

    def build(self):
        for i in range(MAX_SAMPLES):
            value = self.expression.eval(i) % 256
            self.samples.append(value)

    def read(self):
        if self.signal is not None and len(self.samples) > 1024:
            self.signal.emit(np.frombuffer(array.array('B', self.samples[-1024:]).tobytes(), 'int8'))


if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = SpectrogramWidget()
    w.read_collected.connect(w.update)

    output = Samples(w.read_collected)
    output.build()

    interval = FREQUENCY/CHUNK
    t = QtCore.QTimer()
    t.timeout.connect(output.read)
    t.start(interval/1000)

    app.exec_()
