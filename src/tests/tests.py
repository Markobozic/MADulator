import sys
sys.path.append("..")
import keyboard
import pyaudio
import time
from generator import *
from threading import Thread

PyAudio = pyaudio.PyAudio
BITRATE = 11050     #frames per second/frameset.      
LENGTH = 5     #in seconds
NUMBER_OF_FRAMES = int(BITRATE * LENGTH)
REST_FRAMES = NUMBER_OF_FRAMES % BITRATE
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

done = False
gen = Generator(1)
function = gen.random_function()
position = 0

def callback(in_data, frame_count, time_info, status):
    global done
    global playing
    global position
    values = []
    for i in range (position, position + frame_count):
        values.append(chr(function.eval(i) % 256))
    data = ''.join(values)
    position += frame_count
    if keyboard.is_pressed('space'):
        return (data, pyaudio.paComplete)
    if keyboard.is_pressed('esc'):
        done = True
        return (data, pyaudio.paComplete)
    return (data, pyaudio.paContinue)

def main():
    global function
    global done
    while not done:
        print(function)

        # Start audio
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
        function = gen.random_function()

main()
