# -*- coding: utf-8 -*-


import pyaudio
import sys
import pylab
import numpy
import wave


class MyAudio:
    def __init__(self):
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        #self.RECORD_SECONDS = 3
        #WAVE_OUTPUT_FILENAME = "output.wav"
        self.data = None
        self.result = None
        
        self.audio = pyaudio.PyAudio()
        
        self.stream = self.audio.open(format = self.FORMAT,
                             channels = self.CHANNELS,
                             rate = self.RATE,
                             input = True,
                             output = True,
                             frames_per_buffer = self.chunk)
    
    def record(self, record_seconds):
        print "* recording"
        all = []
        for i in range(0, self.RATE / self.chunk * record_seconds):
            self.data = self.stream.read(self.chunk)
            all.append(self.data)
        print "* done recording"
        
        self.data = ''.join(all)
        self.result = numpy.frombuffer(self.data,dtype="int16") / float(2**15)
        
        self.stream.close()
        self.audio.terminate()

    
    def play (self, data, fs, bit):
        import pyaudio
        # ストリームを開く
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
    def save(self, data, fs, bit, filename):
        """波形データをWAVEファイルへ出力"""
        wf = wave.open(filename, "w")
        wf.setnchannels(1)
        wf.setsampwidth(bit / 8)
        wf.setframerate(fs)
        wf.writeframes(data)
        wf.close()
    def plot(self, result):
        pylab.plot(result)
        pylab.ylim([-1, 1])
        pylab.show()
    
if __name__ == '__main__':
    
    ma = MyAudio()
    ma.record(3)
    ma.play(ma.data, 44100, 16)
    ma.save(ma.data, 44100, 16, '../audioDatas/nomal.wav')
    ma.plot(ma.result)