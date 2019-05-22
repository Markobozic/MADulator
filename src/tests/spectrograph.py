"""
Demonstrate the use of layouts to control placement of multiple plots / views /
labels
"""

import sys
sys.path.append("..")
import pyaudio
from generator import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
view = pg.GraphicsView()
layout = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(layout)
view.show()
view.setWindowTitle('MADulator')
view.resize(800,600)

## Instructions
text = "Explore randomly generated sound functions with the arrow keys."
layout.addLabel(text, col=0, colspan=2)
layout.nextRow()

## Add 3 plots into the first row (automatic position)
waveform = layout.addPlot(title="Waveform")
spectrograph = layout.addViewBox(lockAspect=True)
img = pg.ImageItem(np.random.normal(size=(100,100)), title="Spectrograph")
spectrograph.addItem(img)
spectrograph.autoRange()
layout.nextRow()

## Add a sub-layout into the second row (automatic position)
## The added item should avoid the first column, which is already filled
function = layout.addPlot(title="Function", col=0, colspan=2)
function.hideAxis('bottom')
function.hideAxis('left')
text = pg.TextItem("(t+1)", anchor=(0.5, 0.5))
function.addItem(text)
text.setPos(0, 0)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        samples = Samples()
        gen = Generator(1)
        samples.set_expression(gen.random_function)
        p = PyAudio()
        stream = p.open(format = p.get_format_from_width(1), 
            channels = 1, 
            rate = BITRATE, 
            output = True,
            stream_callback=callback)
        stream.start_stream()
        while stream.is_active():
            time.sleep(0.1)
        stream.stop_stream()
        stream.close()
        p.terminate()
        QtGui.QApplication.instance().exec_()

