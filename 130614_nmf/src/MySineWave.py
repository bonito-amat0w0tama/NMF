#!/usr/bin/python
# -*- coding: utf-8 -*-

import wave
import struct
import numpy as np
import pylab as plt


class MySineWave :
    def __init__ (self):
        print "MySineWave_init"
        
    def createSineWave(self, A, f0, fs, length):
        """ A : 振幅
            f0 : 基本周波数
            fs : サンプリング周波数
            length : 長さ（秒）
            """
            
        data = []
        
        
        for i in np.arange(length * fs) :
            s  = A * np.sin(2 *  np.pi * f0 * i/fs)
            
            # 振幅が 1.0以上, -1.0以下だったら
            if s > 1.0 : s = 1.0
            if s < -1.0 : s = -1.0
            data.append(s)
            
        data = [int(x * 32767.0) for x in data]
        #plt.plot(data[:]); plt.show()
        
        
        #data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
        return data
    
    
    def play(self, data, fs, bit):
        import pyaudio
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(fs),
                    output= True)
        # チャンク単位でストリームに出力し音声を再生
        chunk = 1024
        sp = 0  # 再生位置ポインタ
        buffer = data[sp:sp+chunk]
        while buffer != '':
            stream.write(buffer)
            sp = sp + chunk
            buffer = data[sp:sp+chunk]
        stream.close()
        p.terminate()
    def printPlot(self, data):
        plt.plot(data[:500])
        plt.grid()
        plt.show()

        
    
if __name__ == "__main__" :
    
    mys = MySineWave()
    data = mys.createSineWave(1., 440., 44100., 1.)
    mys.printPlot(data)
    #mys.play(data, 44100, 16)
    