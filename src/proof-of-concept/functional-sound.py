import math
import pyaudio
import pygame

PyAudio = pyaudio.PyAudio
BITRATE = 11050     #frames per second/frameset.      
LENGTH = 10     #in seconds
NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

def test_function(t):
    return (t*((t>>12|t>>8)&63&t>>4)) % 256

def main():
    pygame.init()
    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    color = pygame.Color(255,255,255)
    wave_data = []
    for x in range(NUMBEROFFRAMES):
        value = test_function(x)
        x_position = int(x / NUMBEROFFRAMES * WINDOW_WIDTH)
        y_position = int(value / 256 * WINDOW_HEIGHT)
        screen.set_at((x_position, y_position), color)
        wave_data.append(chr(value))

    pygame.display.flip()

    for x in range(RESTFRAMES):
        wave_data.append(chr(128))

    sound_bytes = ''.join(wave_data)
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)

    stream.write(sound_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()

main()
