import math
import pyaudio

PyAudio = pyaudio.PyAudio
BITRATE = 11050     #frames per second/frameset.      
LENGTH = 10     #in seconds

def test_function(t):
    #return (t*((t>>9|t>>1)&25&t>>6)) % 256
    return (t*((t>>12|t>>8)&63&t>>4)) % 256

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''    

#generating wawes
for x in range(NUMBEROFFRAMES):
    WAVEDATA = WAVEDATA+chr(test_function(x))
#result = False

for x in range(RESTFRAMES): 
    WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()
