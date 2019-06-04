import pyaudio as pa
import pickle
import os
from generator import Generator
from samples import Samples
from waveform import Waveform
from editor import Editor
import copy
from spectrogram import *

BITRATE: int = 11025
DEFAULT_VAL: int = 50
MIN_VAL: int = 1
MAX_VAL: int = 2147483647
STEP_VAL: int = 1


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
        self.stream = self.pa.open(format = pa.paUInt8,
            channels = 1,
            rate = BITRATE,
            output = True,
            stream_callback=self.samples.pyaudio_callback)

    def keyPressEvent(self, ev: QtGui.QKeyEvent) -> None:
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Escape:
            # Stop stream and terminate all
            self.terminate_program()
        elif key == QtCore.Qt.Key.Key_Space:
            # Pause/Resume audio stream
            self.pause_resume()
        elif key == QtCore.Qt.Key.Key_R:
            # Restart playback
            self.restart_stream()
        elif key == QtCore.Qt.Key.Key_W:
            # Save waveform
            self.save_wav()
        elif key == QtCore.Qt.Key.Key_S:
            # Save and download a function
            self.save_func()
        elif key == QtCore.Qt.Key.Key_L:
            # Load a function from computer
            self.load_func()
        elif key == QtCore.Qt.Key.Key_BracketLeft:
            # Index through older randomized functions
            self.older_index()
        elif key == QtCore.Qt.Key.Key_BracketRight:
            # Index through newer randomized functions
            self.newer_index()
        elif key == QtCore.Qt.Key.Key_I:
            # Go to a certain function index
            self.get_index()
        elif key == QtCore.Qt.Key.Key_V:
            # Change expression into a Value entered by user
            self.change_to_value()
        elif key == QtCore.Qt.Key.Key_Comma:
            self.samples.slowdown_playback_speed()
        elif key == QtCore.Qt.Key.Key_Period:
            self.samples.increase_playback_speed()
        elif key == QtCore.Qt.Key.Key_Equal:
            self.samples.reset_playback_speed()
        else:
            # Change expression as dictated by user
            is_editor_key = self.editor.new_key(ev.key())
            if is_editor_key:
                self.restart_stream()
            else:
                self.update_editor_info()

    # Key press events
    def terminate_program(self) -> None:
        # Stop stream and terminate all
        if self.stream.is_active():
            self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        QtCore.QCoreApplication.quit()

    def pause_resume(self) -> None:
        if self.stream.is_active():
            self.stream.stop_stream()
        else:
            self.stream.start_stream()

    def save_wav(self) -> None:
        # Save waveform
        duration, ok = QtGui.QInputDialog.getInt(self, "Seconds of Audio:", "Seconds:",
            1, 0, MAX_VAL, STEP_VAL)
        if ok:
            dialog = QtGui.QFileDialog()
            path = dialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'WAV (*.wav)')
            if path[0] != '':
                samples = Samples()
                expression = copy.deepcopy(self.expression)
                samples.set_expression(expression)
                samples.gen_write_16(path[0], duration)

    def save_func(self) -> None:
        # Save and download a function
        dialog = QtGui.QFileDialog()
        path = dialog.getSaveFileName(self, 'Save File', 'save/', 'MAD (*.mad)')
        if path[0] != '':
            with open(path[0], 'wb') as out_file:
                exp = self.samples.get_expression()
                pickle.dump(exp, out_file)

    def load_func(self) -> None:
        # Load a function from computer
        if self.stream.is_active():
            self.stream.stop_stream()
        dialog = QtGui.QFileDialog()
        path = dialog.getOpenFileName(self, 'Open File', 'save/', "MAD (*.mad)")
        if path[0] != '':
            with open(path[0], 'rb') as in_file:
                exp = pickle.load(in_file)
                self.expression = exp
                # Pass a copy to samples
                self.copy_func_to_samples()
                self.editor = Editor(exp)
                # Pass a copy of the expression to editor and display
                self.copy_func_to_editor_and_display()
        self.samples.reset_playback_speed()
        self.stream.start_stream()

    def restart_stream(self) -> None:
        # Stop stream and get reset function
        if self.stream.is_active():
            self.stream.stop_stream()
        expression = self.editor.get_function()
        self.expression = expression
        # Pass a copy to samples, start stream, and display
        self.copy_func_to_samples()
        self.stream.start_stream()
        self.update_editor_info()

    def older_index(self) -> None:
        if self.function_index > 1:
            self.function_index = self.function_index - 1
        self.update_function_from_index()
        self.samples.reset_playback_speed()
        self.index_text.setText("Random function index: " + str(self.function_index))

    def newer_index(self) -> None:
        self.function_index = self.function_index + 1
        self.update_function_from_index()
        self.samples.reset_playback_speed()
        self.index_text.setText("Random function index: " + str(self.function_index))

    def get_index(self) -> None:
        val, ok = QtGui.QInputDialog.getInt(self, "Input Index:", "Index:", 1, 1, 2**30, 1)
        if ok:
            self.function_index = val
            self.index_text.setText("Random function index: " + str(self.function_index))
            self.generator = Generator(self.function_index)
            self.expression = self.generator.random_function()
            self.copy_func_to_samples()
            self.samples.reset_playback_speed()
            self.copy_func_to_editor_and_display()

    def change_to_value(self) -> None:
        # Change expression into a Value entered by user
        val = self.get_number()
        if val != -1:
            self.editor.create_value(val)
            self.restart_stream()
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
            DEFAULT_VAL, MIN_VAL, MAX_VAL, STEP_VAL)
        if ok:
            return val
        return -1

    def setup_layout(self) -> None:
        self.layout = pg.GraphicsLayout(border=(100, 100, 100))
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
        <p><small>Developed by Marko, Angelic, and Daniel</small></p>
        <p>Explore randomly generated sound functions.</p>
        <p><strong>Program keys</strong></p>
        <ul>
        <li>[<span style='color:white'>SPACE</span>] pause or resume playback</li>
		<li>[<span style='color:white'>R</span>] restart playback</li>
        <li>[<span style='color:white'>[</span>] previous random function</li>
        <li>[<span style='color:white'>]</span>] next random function</li>
        <li>[<span style='color:white'>I</span>] goto random function index</li>
        <li>[<span style='color:white'>,</span>] decrease playback speed 10%</li>
        <li>[<span style='color:white'>.</span>] increase playback speed 10%</li>
        <li>[<span style='color:white'>=</span>] restore playback speed to normal</li>
        <li>[<span style='color:white'>S</span>] save function to file</li>
        <li>[<span style='color:white'>L</span>] load function from file</li>
        <li>[<span style='color:white'>W</span>] save audio as .WAV file</li>
        <li>[<span style='color:white'>ESC</span>] exit program</li>
		</ul>
		<p><strong>Function Editor keys</strong></p>
		<ul>
		<li>[<span style='color:white'>↑</span>] Editor: navigate to parent expression</li>
        <li>[<span style='color:white'>←</span>] Editor: navigate to left child expression</li>
        <li>[<span style='color:white'>→</span>] Editor: navigate to right child expression</li>
        <li>[<span style='color:white'>V</span>] replace expression with value (integer)</li>
        <li>[<span style='color:white'>T</span>] replace expression with variable</li>
        <li>[<span style='color:white'>+</span>] replace expression with addition</li>
        <li>[<span style='color:white'>-</span>] replace expression with subtraction</li>
        <li>[<span style='color:white'>*</span>] replace expression with multiplication</li>
        <li>[<span style='color:white'>/</span>] replace expression with integer division</li>
        <li>[<span style='color:white'>%</span>] replace expression with modulo</li>
        <li>[<span style='color:white'>&</span>] replace expression with bitwise AND</li>
        <li>[<span style='color:white'>|</span>] replace expression with bitwise OR</li>
        <li>[<span style='color:white'>^</span>] replace expression with bitwise XOR</li>
        <li>[<span style='color:white'>&lt;</span>] replace expression with shift left</li>
        <li>[<span style='color:white'>></span>] replace expression with shift right</li>
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
