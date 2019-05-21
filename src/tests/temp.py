import numpy as np
import pyqtgraph as pg
import pyaudio
import array
from src.generator import *
from PyQt5 import QtCore, QtGui

FS = 11050 #Hz
CHUNK = 1024 #samples
PyAudio = pyaudio.PyAudio

done = False
gen = Generator()
func = gen.random_function()
position = 0


class DataSupplier:
    def __init__(self, signal):
        self.signal = signal
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt8,
                            channels=1,
                            rate=FS,
                            input=True,
                            output=True,
                            stream_callback=callback)

    # def write(self):
    #     global position
    #     data = []
    #     for i in range(position, position + 10000):
    #         data.append(func.eval(i) % 256)
    #     position += 10000
    #     self.stream.write(array.array('B', data).tobytes(), CHUNK)
    #     print(self.stream.read(CHUNK, exception_on_overflow=False))

    def read(self):
        data = self.stream.read(CHUNK, exception_on_overflow=False)
        y = np.frombuffer(data, 'int8')
        self.signal.emit(y)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


def callback(in_data, frame_count, time_info, status):
    global done, playing, position
    data = []
    for i in range(position, position + frame_count):
        data.append(func.eval(i) % 256)
    position += frame_count
    return array.array('B', data).tostring(), pyaudio.paContinue


class SpectrogramWidget(pg.PlotWidget):

    read_collected = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super(SpectrogramWidget, self).__init__()

        self.img = pg.ImageItem()
        self.addItem(self.img)

        self.img_array = np.zeros((1000, CHUNK//2+1))

        # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,155,255,155], [120,255,0,100], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # set colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([-50, 40])

        # setup the correct scaling for y-axis
        freq = np.arange((CHUNK/2)+1)/(float(CHUNK)/FS)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])
        self.img.scale((1./FS)*CHUNK, yscale)

        self.setLabel('left', 'Frequency', units='Hz')

        # prepare window for later use
        self.win = np.hanning(CHUNK)
        self.show()

    def update(self, chunk):
        # normalized, windowed frequencies in data chunk
        spec = np.fft.rfft(chunk*self.win) / CHUNK
        # get magnitude
        psd = abs(spec)
        # convert to dB scale
        psd = 20 * np.log10(psd)

        # roll down one and replace leading edge with new data
        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = psd

        self.img.setImage(self.img_array, autoLevels=False)


def main():
    app = QtGui.QApplication([])
    w = SpectrogramWidget()
    w.read_collected.connect(w.update)

    data = DataSupplier(w.update)

    # time (seconds) between reads
    interval = FS/CHUNK
    t = QtCore.QTimer()
    # data.read()
    t.timeout.connect(data.read)
    t.start(1000/interval) #QTimer takes ms

    app.exec_()
    data.close()


main()
