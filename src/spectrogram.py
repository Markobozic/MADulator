import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
np.seterr(divide='ignore')

CHUNK = 1024
SPECTROGRAM_WIDTH = 256


class SpectrogramWidget(pg.PlotItem):
    data_available = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, bitrate: int):
        super(SpectrogramWidget, self).__init__()
        self.data_available.connect(self.update)
        self.bitrate = bitrate
        self.img = pg.ImageItem(np.random.normal(size=(100,60)), title="Spectrograph")
        self.addItem(self.img)
        self.img_array = np.zeros((SPECTROGRAM_WIDTH, CHUNK//2+1))

        position = [0.0, 0.25, 0.5, 0.75, 1.0]
        colors = [[0, 0, 0, 255], [0, 0, 256, 255], [256, 0, 0, 255], [242, 125, 0, 255], [253, 207, 88, 255]]
        bi_polar_color_map = pg.ColorMap(position, colors)
        lookup_table = bi_polar_color_map.getLookupTable(0.0, 1.0, 256)

        self.img.setLookupTable(lookup_table)
        self.img.setLevels([0, 5])

        freq = np.arange((CHUNK/2)+1)/(float(CHUNK)/bitrate)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])

        self.img.scale((1./bitrate)*CHUNK, yscale)
        self.setLabel('left', 'Frequency', units='Hz')
        self.win = np.hanning(CHUNK)
        self.show()

    def update(self, chunk: int) -> None:
        magnitude = np.fft.rfft(chunk*self.win) / CHUNK
        abs_mag = abs(magnitude)
        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = abs_mag
        self.img.setImage(self.img_array, autoLevels=False)
