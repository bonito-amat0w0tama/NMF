#/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import wave
import pylab
import struct

#Wavの情報を表示
def printWaveInfo(wf) :
    print "チャンネル数:", wf.getnchannels()
    print "サンプル幅:", wf.getsampwidth()
    print "サンプリング周波数:", wf.getframerate()
    print "フレーム数:", wf.getnframes()
    print "パラメータ:", wf.getparams()
    print "長さ（秒）:", float(wf.getnframes()) / wf.getframerate()


#行列が同じであるかのチェック
def difcost (D1, D2) :
    dif = 0
    
    #行列のすべての行をループ
    for i in range(D1.shape[0]) :
        for j in range(D2.shape[1]) :
            #差の2乗の総和
            dif += pow(D1[i, j] - D2[i, j], 2) #べき乗の計算
    return dif


#因子分解
def factorize (Y, pc, iter) :
    ic, fc = Y.shape #shape関数で行列の行と列の取得
    
    #特徴と重みの行列をランダムな値で初期化
    #列→行の順番でランダムな値で行列を生成
    U = np.matrix ([[np.random.random_sample() for i in range(pc)] 
                    for j in range(ic)])
    H = np.matrix ([[np.random.random_sample() for i in range(fc)]
                    for i in range(pc)])
    print type(H)
    print type(U)
    #最大でiterの回数だけ操作を繰り返す
    for i in range(iter) :
        UH = U * H
        
        #現在の差の計算
        cost = difcost (Y, UH)
        print i, cost
        #行列が完全に因子分解されたら終了
        if cost == 0 :
            break
        
        
        #特徴の行列を更新
        
        #転置した重みの行列にデータ行列を掛け合わせたもの
        Hn = (np.transpose(U) * Y)
        
        #天地した重みの行列に重みの行列を掛け合わせたものに
        #特徴の行列を掛け合わせたもの
        Hd = (np.transpose(U) * U * H)

        #更新
        H = np.matrix(np.array(H) * np.array(Hn) / np.array(Hd))
        
        #重みの行列を更新
        
        #データ行列に転置した特徴の行列を掛け合わせたもの
        Un = Y * H.T
        
        #重みの行列に、特徴の行列を掛け合わせたものに
        #転置した特徴の行列を掛け合わせたもの
        Ud = U * H * H.T

        #更新
        U = np.matrix (np.array(U) * np.array(Un) / np.array(Ud))
        
    return U, H



def play (data, fs, bit):
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
    
# sin波の生成
# A : 振幅, f0 : 基本周波数, fs : サンプリング周波数, length : 再生時間
def createSineWave (A, f0, fs, length):
    data = []
    
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in np.arange(length * fs):  # nはサンプルインデックス
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s) # リストに追加
        
    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    pylab.plot(data[0:100])
    #pylab.show()
    
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data


if __name__ == "__main__" :
    data = createSineWave(1.0, 440, 8000.0, 1.0)
    play(data, 8000, 16)