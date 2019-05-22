from pyqtgraph.Qt import *
import pyqtgraph as pg
import numpy as np
from generator import Generator

class Madulator(pg.GraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = Generator(1)
        self.setup_layout()
        self.setup_spectrograph()
        self.setup_instructions()
        self.setup_editor()

    def keyPressEvent(self, ev: QtGui.QKeyEvent) -> None:
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Escape:
            QtCore.QCoreApplication.quit()
        elif key == QtCore.Qt.Key.Key_R:
            print("randomize function")
        elif key == QtCore.Qt.Key.Key_Space:
            print("Restart playback")

    def setup_layout(self) -> None:
        self.layout = pg.GraphicsLayout(border=(100,100,100))
        self.setCentralItem(self.layout)
        self.show()
        self.setWindowTitle('MADulator')
        self.resize(1024, 720)

    def setup_spectrograph(self) -> None:
        self.spectrograph = self.layout.addViewBox(lockAspect=True)
        img = pg.ImageItem(np.random.normal(size=(100,100)), title="Spectrograph")
        self.spectrograph.addItem(img)
        self.spectrograph.autoRange()
        
    def setup_instructions(self) -> None:
        text = '''
        <h1>MADulator</h1>
        <p>Explore randomly generated sound functions.</p>
        <p><strong>Keys:</strong></p>
        <ul>
        <li>[r] generate random function</li>
        <li>[up] [left] [right] navigate function</li>
        <li>[v] replace expression with value (integer)</li>
        <li>[t] replace expression with variable</li>
        <li>[+] replace expression with addition</li>
        <li>[-] replace expression with subtraction</li>
        <li>[*] replace expression with multiplication</li>
        <li>[/] replace expression with integer division</li>
        <li>[%] replace expression with modulo</li>
        <li>[&] replace expression with bitwise AND</li>
        <li>[|] replace expression with bitwise OR</li>
        <li>[^] replace expression with bitwise XOR</li>
        <li>[space] apply changes / restart playback</li>
        <li>[esc] exit program</li>
        </ul>
        '''
        self.layout.addLabel(text, rowspan=2)
        self.layout.nextRow()

    def setup_editor(self) -> None:
        self.editor_text = pg.LabelItem(name='Test', colspan=2)
        self.layout.addItem(self.editor_text)
        self.editor_text.setText('Function here')
