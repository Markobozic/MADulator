import pyaudio as pa
import numpy as np
import copy
import pickle
from generator import Generator
from samples import Samples
from waveform import Waveform
from spectrogram import *

BITRATE = 11025


class Madulator(pg.GraphicsView):

    function_index = 1
    generator = Generator(function_index)
    expression = generator.random_function()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_layout()
        self.setup_waveform()
        self.setup_instructions()
        self.layout.nextRow()
        self.setup_spectrograph()
        self.layout.nextRow()
        self.setup_editor()
        self.setup_index()
        self.samples = Samples(self.waveform.data_available, self.spectrograph.data_available)
        self.samples.set_expression(self.expression)
        self.randomize_function()
        self.setup_pyaudio()
        self.stream.start_stream()

    def randomize_function(self) -> None:
        self.generator = Generator(self.function_index)
        self.expression = self.generator.random_function()
        self.samples.set_expression(copy.deepcopy(self.expression))
        #self.editor = Editor(copy.deepcopy(self.expression))
        self.editor_text.setText(self.expression.html_tree([self.expression]))

    def setup_pyaudio(self) -> None:
        self.pa = pa.PyAudio()
        self.stream = self.pa.open(format = pa.get_format_from_width(1),
            channels = 1,
            rate = BITRATE,
            output = True,
            stream_callback=self.samples.pyaudio_callback)

    def keyPressEvent(self, ev: QtGui.QKeyEvent) -> None:
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Escape:
            self.stream.stop_stream()
            self.stream.close()
            self.pa.terminate()
            QtCore.QCoreApplication.quit()
        elif key == QtCore.Qt.Key.Key_S:
            dialog = QtGui.QFileDialog()
            path = dialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'MAD (*.mad)')
            if path[0] != '':
                with open(path[0], 'wb') as out_file:
                    exp = self.samples.get_expression()
                    pickle.dump(exp, out_file)
        elif key == QtCore.Qt.Key.Key_L:
            self.stream.stop_stream()
            dialog = QtGui.QFileDialog()
            dialog.setDefaultSuffix('.mad')
            path = dialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
            if path[0] != '':
                with open(path[0], 'rb') as in_file:
                    exp = pickle.load(in_file)
                    self.expression = exp
                    self.samples.set_expression(exp)
                    # self.editor = Editor(exp)
                    # self.editor_text.setText(exp.html_tree([exp])
            self.stream.start_stream()
        elif key == QtCore.Qt.Key.Key_R:
            self.stream.stop_stream()
            self.randomize_function()
            self.stream.start_stream()
        elif key == QtCore.Qt.Key.Key_Space:
            self.stream.stop_stream()
            # Save editor expression to samples
            exp = self.samples.get_expression()
            self.samples.set_expression(exp)
            self.stream.start_stream()
            self.editor_text.setText(str(exp))
        elif key == QtCore.Qt.Key.Key_BracketLeft:
            if self.function_index > 1:
                self.function_index = self.function_index - 1
            self.randomize_function()
            self.index_text.setText("Random function index: " + str(self.function_index))
        elif key == QtCore.Qt.Key.Key_BracketRight:
            self.function_index = self.function_index + 1
            self.randomize_function()
            self.index_text.setText("Random function index: " + str(self.function_index))

    def setup_layout(self) -> None:
        self.layout = pg.GraphicsLayout(border=(100,100,100))
        self.setCentralItem(self.layout)
        self.show()
        self.setWindowTitle('MADulator')
        self.resize(1024, 720)

    def setup_waveform(self) -> None:
        self.waveform = Waveform()
        self.layout.addItem(self.waveform)

    def setup_spectrograph(self) -> None:
        self.spectrograph = SpectrogramWidget(BITRATE)
        self.layout.addItem(self.spectrograph)

    def setup_instructions(self) -> None:
        text = '''
        <h1>MADulator</h1>
        <p>Explore randomly generated sound functions.</p>
        <p><strong>Keys:</strong></p>
        <ul>
        <li>[R] generate random function</li>
        <li>[S] save function to file</li>
        <li>[L] load function from file</li>
        <li>[[] decreate random function index</li>
        <li>[]] increase random function index</li>
        <li>[up] [left] [right] navigate function</li>
        <li>[V] replace expression with value (integer)</li>
        <li>[T] replace expression with variable</li>
        <li>[+] replace expression with addition</li>
        <li>[-] replace expression with subtraction</li>
        <li>[*] replace expression with multiplication</li>
        <li>[/] replace expression with integer division</li>
        <li>[%] replace expression with modulo</li>
        <li>[&] replace expression with bitwise AND</li>
        <li>[|] replace expression with bitwise OR</li>
        <li>[^] replace expression with bitwise XOR</li>
        <li>[SPACE] apply changes / restart playback</li>
        <li>[ESC] exit program</li>
        </ul>
        '''
        self.layout.addLabel(text, rowspan=2)

    def setup_editor(self) -> None:
        self.editor_text = pg.LabelItem(name='Editor')
        self.layout.addItem(self.editor_text)
        self.editor_text.setText(self.expression.html_tree([self.expression]))

    def setup_index(self) -> None:
        self.index_text = pg.LabelItem(name='Index')
        self.layout.addItem(self.index_text)
        self.index_text.setText("Random function index: " + str(self.function_index))
