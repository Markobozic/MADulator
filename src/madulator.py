import pyaudio as pa
import numpy as np
import copy
import pickle
import os
from generator import Generator
from samples import Samples
from waveform import Waveform
from editor import Editor
import copy
from spectrogram import *

BITRATE = 11025
WAV_BITRATE = 44100
default_val: int = 50
min_val: int = 1
max_val: int = 2147483647
step_val: int = 1


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
        self.copy_func_to_samples()
        self.copy_func_to_editor_and_display()
        self.setup_pyaudio()
        self.stream.start_stream()

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
            # Stop stream and terminate all
            self.escape_key_event()
        elif key == QtCore.Qt.Key.Key_W:
            # Save waveform
            self.w_key_event()
        elif key == QtCore.Qt.Key.Key_S:
            # Save and download a function
            self.s_key_event()
        elif key == QtCore.Qt.Key.Key_L:
            # Load a function from computer
            self.l_key_event()
        elif key == QtCore.Qt.Key.Key_Space:
            # Stop stream and get reset function to play from beginning
            self.space_key_event()
        elif key == QtCore.Qt.Key.Key_BracketLeft:
            # Index through older randomized functions
            self.bracket_left_key_event()
        elif key == QtCore.Qt.Key.Key_BracketRight:
            # Index through newer randomized functions
            self.bracket_right_key_event()
        elif key == QtCore.Qt.Key.Key_I:
            # Go to a certain function index
            self.i_key_event()
        elif key == QtCore.Qt.Key.Key_V:
            # Change expression into a Value entered by user
            self.v_key_event()
        else:
            # Change expression as dictated by user
            self.editor.new_key(ev.key())
            self.update_editor_info()

    # Key press events
    def escape_key_event(self) -> None:
        # Stop stream and terminate all
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        QtCore.QCoreApplication.quit()

    def w_key_event(self) -> None:
        # Save waveform
        duration, ok = QtGui.QInputDialog.getInt(self, "Seconds of Audio:", "Seconds:",
            1, 0, max_val, step_val)
        if ok:
            dialog = QtGui.QFileDialog()
            path = dialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'WAV (*.wav)')
            if path[0] != '':
                s = Samples()
                exp = copy.deepcopy(self.expression)
                s.set_expression(exp)
                s.generate_samples_and_write(path[0], duration, BITRATE)

    def s_key_event(self) -> None:
        # Save and download a function
        dialog = QtGui.QFileDialog()
        path = dialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'MAD (*.mad)')
        if path[0] != '':
            with open(path[0], 'wb') as out_file:
                exp = self.samples.get_expression()
                pickle.dump(exp, out_file)

    def l_key_event(self) -> None:
        # Load a function from computer
        self.stream.stop_stream()
        dialog = QtGui.QFileDialog()
        dialog.setDefaultSuffix('.mad')
        path = dialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        if path[0] != '':
            with open(path[0], 'rb') as in_file:
                exp = pickle.load(in_file)
                self.expression = exp
                # Pass a copy to samples
                self.copy_func_to_samples()
                self.editor = Editor(exp)
                # Pass a copy of the expression to editor and display
                self.copy_func_to_editor_and_display()
        self.stream.start_stream()

    def space_key_event(self) -> None:
        # Stop stream and get reset function
        self.stream.stop_stream()
        selection = self.editor.get_selection()
        exp = self.editor.get_function()
        self.expression = exp
        # Pass a copy to samples, start stream, and display
        self.copy_func_to_samples()
        self.stream.start_stream()
        self.update_editor_info()

    def bracket_left_key_event(self) -> None:
        if self.function_index > 1:
            self.function_index = self.function_index - 1
        self.update_function_from_index()
        self.index_text.setText("Random function index: " + str(self.function_index))

    def bracket_right_key_event(self) -> None:
        self.function_index = self.function_index + 1
        self.update_function_from_index()
        self.index_text.setText("Random function index: " + str(self.function_index))

    def i_key_event(self) -> None:
        val, ok = QtGui.QInputDialog.getInt(self, "Input Index:", "Index:", 1, 1, 2**30, 1)
        if ok:
            self.function_index = val
            self.index_text.setText("Random function index: " + str(self.function_index))
            self.generator = Generator(self.function_index)
            self.expression = self.generator.random_function()
            self.copy_func_to_samples()
            self.copy_func_to_editor_and_display()

    def v_key_event(self) -> None:
        # Change expression into a Value entered by user
        val = self.get_number()
        if val != -1:
            self.editor.create_value(val)
        self.update_editor_info()

    def update_function_from_index(self) -> None:
        self.generator = Generator(self.function_index)
        self.expression = self.generator.random_function()
        self.copy_func_to_samples()
        self.copy_func_to_editor_and_display()

    def update_editor_info(self) -> None:
        selection = self.editor.get_selection()
        expression = self.editor.get_function()
        self.editor_text.setText(expression.html_tree(selection))

    def copy_func_to_samples(self) -> None:
        expression = copy.deepcopy(self.expression)
        self.samples.set_expression(expression)

    def copy_func_to_editor_and_display(self) -> None:
        function = copy.deepcopy(self.expression)
        self.editor.set_function(function)
        self.update_editor_info()

    def get_number(self) -> int:
        val, ok = QtGui.QInputDialog.getInt(self, "Input Value:", "Value:",
            default_val, min_val, max_val, step_val)
        if ok:
            return val
        return -1

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
        <li>[W] save audio as .WAV file</li>
        <li>[S] save function to file</li>
        <li>[L] load function from file</li>
        <li>[[] decreate random function index</li>
        <li>[]] increase random function index</li>
        <li>[I] goto function index</li>
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
        <li>[&lt;] replace expression with shift left</li>
        <li>[>] replace expression with shift right</li>
        <li>[SPACE] apply changes / restart playback</li>
	    <li>[ESC] exit program</li>
        </ul>
        '''
        self.layout.addLabel(text, rowspan=2)

    def setup_editor(self) -> None:
        function = copy.deepcopy(self.expression)
        self.editor = Editor(function)
        self.editor_text = pg.LabelItem(name='Editor')
        self.layout.addItem(self.editor_text)
        self.update_editor_info()

    def setup_index(self) -> None:
        self.index_text = pg.LabelItem(name='Index')
        self.layout.addItem(self.index_text)
        self.index_text.setText("Random function index: " + str(self.function_index))
