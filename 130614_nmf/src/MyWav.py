#!/usr/bin/python
# -*- coding: utf-8 -*-

import wave
#import pyaudio
import numpy as np
import pylab as plt

class MyWav :
    def __init__(self, audioName):
        self.wf = wave.open(audioName, "r")
        buffer = self.wf.readframes(self.wf.getnframes()) # <type 'str'>, バッファーへ読み込み
        self.data = plt.frombuffer(buffer, dtype = "int16") # <type 'numpy.ndarray'>の変数へ代入
        
        
        self.Y = None
        self.freqs = None
        self.bins = None
        
        
        print ("MyWav_init")
        
        
    def printWaveInfo(self):    
        print "チャンネル数:", self.wf.getnchannels()
        print "サンプル幅:", self.wf.getsampwidth()
        print "サンプリング周波数:", self.wf.getframerate()
        print "フレーム数:", self.wf.getnframes()
        print "パラメータ:", self.wf.getparams()
        print "長さ（秒）:", float(self.wf.getnframes()) / self.wf.getframerate()
    
    def getDataLength(self):
        print "dataLength",len(self.data)
    
    def printAllPlot(self):
        #print len(self.data)
        plt.plot(self.data[:])
        plt.show()
    
    def printPlot(self, start, end):
        #print len(self.data)
        plt.plot(self.data[start : end])
        plt.grid()
        plt.show()
    
    def plotSpecgram(self):
        N = 512 # 窓長
        hamming = np.hamming(N) # Hamming_windowの作成

        # スペクトログラムの作成,表示
        plt.figure(1)
        plt.suptitle('Spectrogram')
        plt.xlabel('time [sec]')
        plt.ylabel('freqency [Hz]')
        
        # specgram(データ, 窓長, サンプリング周波数, オーバーラップの長さ, 窓関数)??
        self.Y, self.freqs, self.bins, im = plt.specgram(self.data, NFFT = N, Fs = self.wf.getframerate(), 
                                            noverlap = 0, window = hamming)
        plt.savefig('../picDatas/specgram.png', format = 'png')

    def showPlot(self):
        plt.show()


if __name__ == '__main__':
    
    mywav = MyWav("../audioDatas/guitar.wav")
    mywav.printWaveInfo()
    #mywav.printAllPlot()
    mywav.printPlot(0, 500)
    mywav.getDataLength()
    mywav.plotSpecgram()
    mywav.showPlot()
    