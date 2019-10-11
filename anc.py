import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

# constants (can be set lower (worse) or higher (better) depending on hardware)
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))
plt.axhline(y=128,linestyle='--', color='gray')

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=1, mec=(255,0,0,1))
line_mirror, = ax.plot(x, np.random.rand(CHUNK), '-', lw=1, mec=(0,0,255,1))

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('amplitude')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[], yticks=[])

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:
    
    # binary data
    data = stream.read(CHUNK)  
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128 
    data_np_mirror = 128 - (data_np - 128)

    line.set_ydata(data_np)
    line_mirror.set_ydata(data_np_mirror)
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break