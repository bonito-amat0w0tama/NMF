#/usr/bin/python2.7
# -*_ coding: utf-8 -*-

from defs import *

if __name__ == "__main__" :
    #Mat = np.random.random_sample(2 * 3).reshape(2, 3)
    
    #U, H = factorize (Mat, pc = 4, iter = 100)
    
    wf = wave.open("../audioDatas/guitar.wav", "rb")
    printWaveInfo(wf)
    
    
    
    buffer = wf.readframes(wf.getnframes()) #バッファに一時保存
    print len(buffer) #bufferの長さ
    
    data = pylab.frombuffer(buffer, dtype = "int16") # int16 : 量子化精度
    N = 512
    hamming = np.hamming(N)
    
    # play(data, wf.getframerate(), 16)
    
    # スペクトログラムの作成,表示
    pylab.figure(1)
    pylab.suptitle('Spectrogram')
    pylab.xlabel('time [sec]')
    pylab.ylabel('freqency [Hz]')
    
    # specgram(データ, 窓長, サンプリング周波数, オーバーラップの長さ, 窓関数)??
    Y, freqs, bins, im = pylab.specgram(data, NFFT = N, Fs = wf.getframerate(), 
                                        noverlap = 0, window = hamming)
    pylab.savefig('../picDatas/specgram.png', format = 'png')
    
    # NMFに使うパラメーター
    nBase =  20 # 基底, 特徴量
    iter = 300
    row, col = Y.shape
    H, U = factorize(Y, nBase, iter)
    
    # np.array型に変換
    H = np.array(H)
    U = np.array(U)
       
    # H, Uの表示
    pylab.figure(2)
    pylab.suptitle('H (left) and U (right)')
    count = 1
    print freqs.shape, H.shape
    for i in range(nBase - 1) :
        a = pylab.subplot(nBase, 2, count)
        a.tick_params(labelleft='off',labelbottom='off')
        pylab.plot(freqs,H[:,i])
        b = pylab.subplot(nBase,2,count+1)
        b.tick_params(labelleft='off',labelbottom='off')
        pylab.plot(bins, U[i,:])
        count += 2

    a = pylab.subplot(nBase,2,count)
    a.tick_params(labelleft='off')
    pylab.plot(freqs,H[:,i])
    pylab.xlabel('freqency [Hz]')
    b = pylab.subplot(nBase,2,count+1)
    b.tick_params(labelleft='off')        
    pylab.plot(bins,U[i,:])
    pylab.xlabel('time [sec]')        
    pylab.savefig('../picDatas/result.png',format='png')

    pylab.show()