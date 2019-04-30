import math
import pyaudio
import pygame
import time
from datetime import datetime, timedelta
from threading import Thread

PyAudio = pyaudio.PyAudio
BITRATE = 11050     #frames per second/frameset.      
LENGTH = 15     #in seconds
NUMBER_OF_FRAMES = int(BITRATE * LENGTH)
REST_FRAMES = NUMBER_OF_FRAMES % BITRATE
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512
PIXEL_SIZE = 2

def test_function(t):
    return (t*((t>>12|t>>8)&63&t>>4)) % 256

def play_audio(sound_bytes):
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)
    time.sleep(1)
    stream.write(sound_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    # Generate values
    values = []
    print("\nGenerating values...")
    for x in range(NUMBER_OF_FRAMES + REST_FRAMES):
        if(x%1000==0):
            print('*',end='')
        values.append(test_function(x))

    # Generate wave data
    wave_data = []
    print("\nGenerating audio...")
    for i in range(len(values)):
        if(i%1000==0):
            print('*',end='')
        wave_data.append(chr(values[i]))
    sound_bytes = ''.join(wave_data)
    
    # Start audio
    t = Thread(target=play_audio, args=(sound_bytes,))
    t.start()


    # Show graphics
    pygame.init()
    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    color = pygame.Color(255,255,255,10)
    start_time = datetime.now()
    time_of_last_redraw = start_time
    desired_redraw_interval = 1/30.0
    values_length = len(values)
    counter = 0
    pixel_brush = pygame.Surface((PIXEL_SIZE,PIXEL_SIZE))
    pixel_brush.set_alpha(32)
    pixel_brush.fill((255,255,255))
    for i in range(values_length):
        current_time = datetime.now()
        time_progress = (current_time-start_time).total_seconds()/LENGTH
        graphics_progress = i/NUMBER_OF_FRAMES
        while(graphics_progress > time_progress):
            time.sleep(.0001)
            current_time = datetime.now()
            time_progress = (current_time-start_time).total_seconds()/LENGTH
        x_position = int(graphics_progress * WINDOW_WIDTH)
        y_position = int(values[i] / 256 * WINDOW_HEIGHT)
        screen.blit(pixel_brush, (x_position, y_position))
        if((current_time-time_of_last_redraw).total_seconds() > desired_redraw_interval):
            pygame.display.flip()
            time_of_last_redraw = current_time

main()
