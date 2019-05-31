from pyqtgraph.Qt import QtCore, QtGui
from expression import *
from pyaudio import *
import threading
import numpy as np
import wave
import struct

BITRATE: int = 11025
WAV_BITRATE: int = 44100
SAMPLES_TO_EMIT_LENGTH: int = 1024

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
            val = struct.pack('B', value)
            sound_samples.append(val)
        data = b''.join(sound_samples)
        self.position += frame_count
        try:
            if (self.waveform_signal is not None and self.spectrogram_signal is not None) and len(self.samples) >= SAMPLES_TO_EMIT_LENGTH:
                self.emit_waveform_signal()
                self.emit_spectrogram_signal()
        finally:
            self.lock.release()
        return data, paContinue

    def gen_write_16(self, filename: str, duration: int) -> None:
        ratio = WAV_BITRATE/BITRATE
        num_samples = duration * WAV_BITRATE
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

    def get_expression(self) -> Expression:
        return self.expression

    def set_expression(self, expression: Expression) -> None:
        self.lock.acquire()
        self.expression = expression
        self.lock.release()
        self.reset()

    def reset(self) -> None:
        self.lock.acquire()
        self.position = 0
        self.samples.clear()
        self.lock.release()

    def emit_waveform_signal(self):
        self.waveform_signal.emit(self.samples[-SAMPLES_TO_EMIT_LENGTH:])

    def emit_spectrogram_signal(self):
        self.spectrogram_signal.emit(np.asarray(self.samples[-SAMPLES_TO_EMIT_LENGTH:]))
