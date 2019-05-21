from pyqtgraph.Qt import QtCore
import expression import *
from pyaudio import *

class Function():

    def __init__(self, signal1):
        self.expression = Expression()
        self.signal1 = signal1
        self.samples = []
        self.position = 0

    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        for i in range(self.position, self.position + frame_count):
            value = self.expression.eval(i) % 256
            self.samples.append(value)
        data = ''.join(self.samples[-frame_count:]
        self.position += frame_count
        self.signal.emit(self.samples[-1024:])
        return data, pyaudio.paContinue

    def set_expression(self, expression):
        self.expression = expression
        self.reset()

    def reset(self):
        self.samples.clear()
        self.position = 0
