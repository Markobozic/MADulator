import keyboard
import pyaudio
import time
import array
from src.generator import *
from threading import Thread

PyAudio = pyaudio.PyAudio
BITRATE = 11050     #frames per second/frameset.      
LENGTH = 5     #in seconds
NUMBER_OF_FRAMES = int(BITRATE * LENGTH)
REST_FRAMES = NUMBER_OF_FRAMES % BITRATE
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

done = False
gen = Generator()
func = gen.random_function()
position = 0


# def callback(in_data, frame_count, time_info, status):
#     global done
#     global playing
#     global position
#     data = []
#     for i in range(position, position + frame_count):
#         data.append(function.eval(i) % 256)
#     print(data)
#     position += frame_count
#     if keyboard.is_pressed('space'):
#         return data, pyaudio.paComplete
#     if keyboard.is_pressed('esc'):
#         done = True
#         return data, pyaudio.paComplete
#     return data, pyaudio.paContinue

def callback(in_data, frame_count, time_info, status):
    global done, playing, position
    data = []
    for i in range(position, position + frame_count):
        data.append(func.eval(i) % 256)
    position += frame_count
    print(array.array('B', data).tostring())
    return array.array('B', data).tostring(), pyaudio.paContinue

def main():
    global func
    global done
    while not done:
        print(func)

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
        func = gen.random_function()


main()
