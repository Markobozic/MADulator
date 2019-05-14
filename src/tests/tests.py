import pyaudio
import sys
sys.path.append("..")
from generator import *
from threading import Thread

PyAudio = pyaudio.PyAudio
BITRATE = 11050     #frames per second/frameset.      
LENGTH = 5     #in seconds
NUMBER_OF_FRAMES = int(BITRATE * LENGTH)
REST_FRAMES = NUMBER_OF_FRAMES % BITRATE
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

def play_audio(sound_bytes):
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)
    stream.write(sound_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    # Generate values
    gen = Generator(1)
    done = False
    while not done:
        function = gen.random_function()
        print(function)
        values = []
        for x in range(NUMBER_OF_FRAMES + REST_FRAMES):
            values.append(function.eval(x) % 256)

        # Generate wave data
        wave_data = []
        for i in range(len(values)):
            wave_data.append(chr(values[i]))
        sound_bytes = ''.join(wave_data)
        
        # Start audio
        t = Thread(target=play_audio, args=(sound_bytes,))
        t.start()
        print()
        choice = input("Press 'enter' to generate another function, or enter 'x' to quit.")
        if choice == 'x':
            done = True

main()
