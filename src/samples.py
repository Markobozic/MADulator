from src.expression import *
from pyaudio import *
import numpy as np
import array
import pyqtgraph as pg
from src.generator import *
from PyQt5 import QtCore, QtGui

FS = 11025 #Hz

CHUNKSZ = 1024 #samples

class Samples:

    def __init__(self, signal: QtCore.pyqtSignal = None):
        self.expression = Generator(1).random_function()
        self.signal = signal
        self.samples = []
        self.position = 0
        self.temp = self.pyaudio_callback

    def pyaudio_callback(self, in_data, frame_count, time_info, status) -> (str, int):
        sound_samples = []
        for i in range(self.position, self.position + frame_count):
            value = self.expression.eval(i) % 256
            self.samples.append(value)
            sound_samples.append(chr(value))
            print(sound_samples)
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

    def build(self):
        for i in range(self.position, self.position + 100000):
            value = self.expression.eval(i) % 256
            self.samples.append(value)
        self.position += 4096
        print(len(self.samples))

    def read(self):
        # sound_samples = []
        # for i in range(self.position, self.position + 1024):
        #     value = self.expression.eval(i) % 256
        #     self.samples.append(value)
        # data = ''.join(self.samples)
        # self.position += 1024
        if self.signal is not None and len(self.samples) > 1024:
            self.signal.emit(np.frombuffer(array.array('B', self.samples[-1024:]).tobytes(), 'int8'))
            print(self.samples[-1024:])
            del self.samples[:1024]
        self.build()


class SpectrogramWidget(pg.PlotWidget):
    read_collected = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super(SpectrogramWidget, self).__init__()

        self.img = pg.ImageItem()
        self.addItem(self.img)

        self.img_array = np.zeros((1000, CHUNKSZ//2+1))

        # bipolar colormap

        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        self.img.setLookupTable(lut)
        self.img.setLevels([-50,40])

        freq = np.arange((CHUNKSZ/2)+1)/(float(CHUNKSZ)/FS)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])
        self.img.scale((1./FS)*CHUNKSZ, yscale)

        self.setLabel('left', 'Frequency', units='Hz')

        self.win = np.hanning(CHUNKSZ)
        self.show()

    def update(self, chunk):
        # normalized, windowed frequencies in data chunk

        spec = np.fft.rfft(chunk*self.win) / CHUNKSZ
        # get magnitude

        psd = abs(spec)
        # convert to dB scale

        psd = 20 * np.log10(psd)

        # roll down one and replace leading edge with new data

        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = psd

        self.img.setImage(self.img_array, autoLevels=False)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = SpectrogramWidget()
    w.read_collected.connect(w.update)

    output = Samples(w.read_collected)
    output.build()
    # temp = output.read()
    # print(temp)
    # time (seconds) between reads

    interval = FS/CHUNKSZ
    t = QtCore.QTimer()
    t.timeout.connect(output.read)
    t.start(1000/interval) #QTimer takes ms


    app.exec_()
    # mic.close()
