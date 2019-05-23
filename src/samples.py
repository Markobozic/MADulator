from pyqtgraph.Qt import QtCore
from expression import *
from pyaudio import *

class Samples():

    def __init__(self, signal: QtCore.pyqtSignal = None):
        self.expression = Expression()
        self.signal = signal
        self.samples = []
        self.position = 0

    def pyaudio_callback(self, in_data, frame_count, time_info, status) -> (str, int):
        sound_samples = []
        for i in range(self.position, self.position + frame_count):
            value = self.expression.eval(i) % 256
            self.samples.append(value)
            sound_samples.append(chr(value))
        data = ''.join(sound_samples)
        self.position += frame_count
        if self.signal is not None and len(self.samples) > 1024:
            self.signal.emit(self.samples[-1024:])
        return data, paContinue

    def get_expression(self) -> Expression:
        return self.expression

    def set_expression(self, expression: Expression) -> None:
        self.expression = expression
        self.reset()

    def reset(self) -> None:
        self.position = 0
        self.samples.clear()
