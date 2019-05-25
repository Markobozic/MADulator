import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui

FREQUENCY = 11025
CHUNK = 1024


class SpectrogramWidget(pg.PlotWidget):
    read_collected = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super(SpectrogramWidget, self).__init__()
        self.img = pg.ImageItem()
        self.addItem(self.img)
        self.img_array = np.zeros((1000, CHUNK//2+1))

        position = np.array([0., 1., 0.5, 0.25, 0.75])
        colors = np.array([[0, 255, 255, 255], [255, 255, 0, 255], [0, 0, 0, 255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        bi_polar_color_map = pg.ColorMap(position, colors)
        lookup_table = bi_polar_color_map.getLookupTable(0.0, 1.0, 256)

        self.img.setLookupTable(lookup_table)
        self.img.setLevels([-50, 40])

        freq = np.arange((CHUNK/2)+1)/(float(CHUNK)/FREQUENCY)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])

        self.img.scale((1./FREQUENCY)*CHUNK, yscale)
        self.setLabel('left', 'Frequency', units='Hz')
        self.win = np.hanning(CHUNK)
        self.show()

    def update(self, chunk):
        magnitude = np.fft.rfft(chunk*self.win) / CHUNK
        magnitude_in_db_scale = 20 * np.log10(abs(magnitude))

        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = magnitude_in_db_scale
        self.img.setImage(self.img_array, autoLevels=False)
