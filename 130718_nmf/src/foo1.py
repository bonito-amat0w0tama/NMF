# -*- coding: utf-8 -*-


import pyaudio
import sys
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct
import copy


class MyAudio:
    def __init__(self):
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        #self.RECORD_SECONDS = 3
        #WAVE_OUTPUT_FILENAME = "output.wav"
        self.data = None
        self.disData = None
        self.result = None
        
        self.audio = pyaudio.PyAudio()
        
#         self.stream = self.audio.open(format = self.FORMAT,
#                              channels = self.CHANNELS,
#                              rate = self.RATE,
#                              input = True,
#                              output = True,
#                              frames_per_buffer = self.chunk)
    
    def record(self, record_seconds):
        
        stream = self.audio.open(format = self.FORMAT,
                             channels = self.CHANNELS,
                             rate = self.RATE,
                             input = True,
                             frames_per_buffer = self.chunk)
        
        
        print "* recording"
        all = []
        for i in range(0, self.RATE / self.chunk * record_seconds):
            self.data = stream.read(self.chunk)
            all.append(self.data)
        print "* done recording"
        
        self.data = ''.join(all)
        #self.result = np.frombuffer(self.data,dtype="int16") / float(2**15)
        
        stream.close()
    def play (self, data, fs, bit):
        import pyaudio
        # ストリームを開く
        #p = pyaudio.PyAudio()
        stream = self.audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=int(fs),
                        output= True)
        # チャンク単位でストリームに出力し音声を再生
        chunk = 1024
        sp = 0  # 再生位置ポインタ
        buffer = data[sp:sp+chunk]
        while stream.is_active():
            stream.write(buffer)
            sp += chunk
            buffer = data[sp:sp+chunk]
            if buffer == '': stream.stop_stream()
        stream.close()
    def save(self, data, fs, bit, filename):
        """波形データをWAVEファイルへ出力"""
        wf = wave.open(filename, "w")
        wf.setnchannels(1)
        wf.setsampwidth(bit / 8)
        wf.setframerate(fs)
        wf.writeframes(data)
        wf.close()
    
    def plot(self, data1, data2, data3, data4):
        
        result1 = copy.deepcopy(data1)
        result2 = copy.deepcopy(data2)
        result3 = copy.deepcopy(data3)
        result4 = copy.deepcopy(data4)
        
        #print type(result1)
        if type(result1) == str :
            result1 = np.frombuffer(result1,dtype="int16") / float(2**15)
        if type(result2) == str :
            result2 = np.frombuffer(result2,dtype="int16") / float(2**15)
        if type(result3) == str :
            result3 = np.frombuffer(result3,dtype="int16") / float(2**15)
        if type(result4) == str :
            result3 = np.frombuffer(result4,dtype="int16") / float(2**15)
            
            
        print type(result1)
        print type(result2)
        # オリジナル波形の一部をプロット
        plt.subplot(221)
        plt.plot(result1)
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        plt.ylim([-1.0, 1.0])
    
        # サウンドエフェクトをかけた波形の一部をプロット
        plt.subplot(222)
        plt.plot(result2)
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        plt.ylim([-1.0, 1.0])
        
        plt.subplot(223)
        plt.plot(result3)
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        plt.ylim([-1.0, 1.0])
        
        plt.subplot(224)
        plt.plot(result4)
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        plt.ylim([-1.0, 1.0])
        
        plt.show()
        
    def distorsion(self, data, gain, level):
        data2 = copy.deepcopy(data)
        print type(data2)
        if type(data2) == str :
            data2 = np.frombuffer(data2, dtype="int16") / 32768.0
            print type(data2)
        length = len(data2)
        newdata = [0.0] * length
        for i in range(length):
            newdata[i] = data[i] * gain # 増幅
            # クリッピング
            if newdata[i] > 1.0:
                newdata[i] = 1.0
            elif newdata[i] < -1.0:
                newdata[i] = -1.0
            
            # 音量を調整
            newdata[i] *= level
        
#         newdata = [int(x * 32767.0) for x in newdata]
#         newdata = struct.pack("h" * len(newdata), *newdata)
        return newdata
        
    def end(self):
        self.audio.terminate()
        print "end"
    
    
    def delay(self, wf):
        fs = wf.getframerate()      # サンプリング周波数
        length = wf.getnframes()    # 総フレーム数
        data = wf.readframes(length)
    
        data = np.frombuffer(data, dtype="int16") / 32768.0  # -1 - +1に正規化
        a = 0.6      # 減衰率
        d = 20000    # 遅延時間（単位：サンプル）
        repeat = 3   # リピート回数
    
        newdata = [0.0] * length
        for n in range(length):
            newdata[n] = data[n]
            # 元のデータに残響を加える
            for i in range(1, repeat + 1):
                m = int(n - i * d)
                if m >= 0:
                    newdata[n] += (a ** i) * data[m]  # i*dだけ前のデータを減衰させた振幅を加える
                    
        return newdata
    def reverve(self, wf):
        fs = wf.getframerate()      # サンプリング周波数
        length = wf.getnframes()    # 総フレーム数
        data = wf.readframes(length)

    
        data = np.frombuffer(data, dtype="int16") / 32768.0  # -1 - +1に正規化
        a = 0.7      # 減衰率
        repeat = 3   # リピート回数
    
        alldata = ''
        for d in range(1000, 3000, 500):  # 遅延時間d(sample) を変えながら音を鳴らす
            newdata = [0.0] * length
            for n in range(length):
                newdata[n] = data[n]
                # 元のデータに残響を加える
                for i in range(1, repeat + 1):
                    m = int(n - i * d)
                    if m >= 0:
                        newdata[n] += (a ** i) * data[m]  # i*dだけ前のデータを減衰させた振幅を加える
        return newdata
    
    def bar(self, data):
        for x in data:
            if x > 326767.0:
                print hello
    
            
if __name__ == '__main__':
    
    ma = MyAudio()
    ma.record(8)
    ma.play(ma.data, 44100, 16)
    ma.save(ma.data, 44100, 16, '../audioDatas/nomal.wav')
    
    wf = wave.open('../audioDatas/nomal.wav', 'r')
    delay = ma.delay(wf)
       
    wf = wave.open('../audioDatas/nomal.wav', 'r')
    reverve = ma.reverve(wf)
    
    ma.data = np.frombuffer(ma.data, dtype="int16") / 32768.0
    distosion = ma.distorsion(ma.data, 200, 0.3)

    ma.plot(ma.data, distosion, delay, reverve)
    
    print len(delay)
    
#     delay = [int(x * 32767.0) for x in delay]
#     ma.bar(delay)
#     delay = struct.pack("h" * len(delay), *delay)
#     ma.save(delay, 44100, 16, '../audioDatas/delay.wav')
    
    reverve = [int(x * 32767.0) for x in reverve]
    reverve = struct.pack("h" * len(reverve), *reverve)
    ma.save(reverve, 44100, 16, '../audioDatas/reverve.wav')
    
    distosion = [int(x * 32767.0) for x in distosion]
    distosion = struct.pack("h" * len(distosion), *distosion)
    ma.save(distosion, 44100, 16, '../audioDatas/distosion.wav')
 

    ma.end()