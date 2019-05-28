from pyqtgraph.Qt import QtCore
from expression import *
from pyaudio import *
import threading
import numpy as np


class Samples:

    def __init__(self, waveform_signal: QtCore.pyqtSignal = None, spectrogram_signal: QtCore.pyqtSignal = None):
        self.expression = Expression()
        self.lock = threading.Lock()
        self.waveform_signal = waveform_signal
        self.spectrogram_signal = spectrogram_signal
        self.samples = []
        self.position = 0

    def pyaudio_callback(self, in_data, frame_count, time_info, status) -> (str, int):
        self.lock.acquire()
        sound_samples = []
        for i in range(self.position, self.position + frame_count):
            value = self.expression.eval(i) % 256
            self.samples.append(value)
            sound_samples.append(chr(value))
        data = ''.join(sound_samples)
        self.position += frame_count
        try:
            if (self.waveform_signal is not None and self.spectrogram_signal is not None) and len(self.samples) >= 1024:
                self.waveform_signal.emit(self.samples[-1024:])
                self.spectrogram_signal.emit(np.asarray(self.samples[-1024:]))
        finally:
            self.lock.release()
        return data, paContinue

    def get_expression(self) -> Expression:
        return self.expression

    def set_expression(self, expression: Expression) -> None:
        self.lock.acquire()
        self.expression = expression
        self.reset()

    def reset(self) -> None:
        self.position = 0
        self.lock.release()
        self.samples.clear()
