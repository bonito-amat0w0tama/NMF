#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wave
from numpy import *

freq = 44100
t = linspace(0.0,1.0,freq)
amp = 15000


w = amp*(sin(2000*2*pi*t)+sin(2002*2*pi*t))/2
data = w.astype(int16)
out = wave.open('mono.wav','w')
out.setnchannels(1) #mono
out.setsampwidth(2) #16bits
out.setframerate(freq)
out.writeframes(data.tostring())
out.close()


wL = amp*sin(2000*2*pi*t)
wR = amp*sin(2002*2*pi*t)
w = array([wL,wR]).transpose()
data = w.astype(int16)
out = wave.open('stereo.wav','w')
out.setnchannels(2) #stereo
out.setsampwidth(2) #16bits
out.setframerate(freq)
out.writeframes(data.tostring())
out.close()


