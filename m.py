#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy
import math
import matplotlib.pyplot as plt
import matplotlib.animation
import wave
# import soundfile

RATE = 44100
BUFFER = 882

# data,fs=soundfile.read('ald.wav', dtype='float32')

filename = 'ald.wav'
chunk = 1024
wf = wave.open(filename, 'rb')

p = pyaudio.PyAudio()

stream = p.open(
    format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read in the frames as data
data = wf.readframes(chunk)

fig = plt.figure()
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

RATE = wf.getframerate()
BUFFER = chunk

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line(i):
    try:
        dataraw = wf.readframes(chunk)
        stream.write(dataraw)
        datafin = stream.read(chunk)

        
        data = numpy.fft.rfft(numpy.fromstring(
            datafin, dtype=numpy.float32)
        )

        try:
            data = numpy.log10(numpy.sqrt(
            numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10
        except:
            pass
        line1.set_data(r, data)
        line2.set_data(numpy.maximum(line1.get_data(), line2.get_data()))
        return (line1,line2,)
    except IOError:
        pass
        return (line1,line2,)
    
    
    

plt.xlim(0, RATE/2+1)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

line_ani = matplotlib.animation.FuncAnimation(
    fig, update_line, init_func=init_line, interval=0, blit=True
)

plt.show()

