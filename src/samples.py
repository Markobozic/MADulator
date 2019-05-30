from pyqtgraph.Qt import QtCore, QtGui
from expression import *
from pyaudio import *
import array
import numpy as np
import wave
import struct
import math

BITRATE = 11025
WAV_BITRATE = 44100

class Samples:

    def __init__(self, waveform_signal: QtCore.pyqtSignal = None, spectrogram_signal: QtCore.pyqtSignal = None):
        self.expression = Expression()
        self.waveform_signal = waveform_signal
        self.spectrogram_signal = spectrogram_signal
        self.samples = []
        self.position = 0

    def pyaudio_callback(self, in_data, frame_count, time_info, status) -> (bytes, int):
        sound_samples = []
        for i in range(self.position, self.position + frame_count):
            value = self.expression.eval(i) % 256
            self.samples.append(value)
            val = struct.pack('B', value)
            sound_samples.append(val)
        data = b''.join(sound_samples)
        self.position += frame_count
        if (self.waveform_signal and self.spectrogram_signal) is not None and len(self.samples) > 1024:
            self.waveform_signal.emit(self.samples[-1024:])
            self.spectrogram_signal.emit(np.frombuffer(array.array('B', self.samples[-1024:]).tobytes(), 'int8'))
        return data, paContinue

    def gen_write_8(self, filename: str, duration: int) -> None:
        num_samples = duration * BITRATE
        print(num_samples)
        sample = []
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(1)
        wave_file.setframerate(BITRATE)
        for i in range(num_samples):
            one = self.expression.eval(i) % 256
            sample = struct.pack('B', one)
            wave_file.writeframesraw(sample)
        wave_file.writeframes(b'')
        wave_file.close()

    def gen_write_16(self, filename: str, duration: int) -> None:
        ratio = WAV_BITRATE/BITRATE
        num_samples = duration * WAV_BITRATE
        print(num_samples)
        sample = []
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)
        wave_file.setframerate(WAV_BITRATE)
        for i in range(num_samples):
            one = self.expression.eval(int(i/ratio)) % 256
            one = (one * 256) - 2**15
            sample = struct.pack('<h', one)
            wave_file.writeframesraw(sample)
        wave_file.writeframes(b'')
        wave_file.close()

    def get_samples(self) -> list:
        return self.samples

    def get_expression(self) -> Expression:
        return self.expression

    def set_expression(self, expression: Expression) -> None:
        self.expression = expression
        self.reset()

    def reset(self) -> None:
        self.position = 0
        self.samples.clear()
