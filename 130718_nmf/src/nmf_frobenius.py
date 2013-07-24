#/usr/bin/python
# coding: utf-8

import wave
import numpy as np
from pylab import *


def difcost_by_frobenius (Y, HU) :
        dif = 0
        cY = np.matrix(Y)
        cHU = np.matrix(HU)
        
        # 行列のすべての行をループ
        for i in range(Y.shape[0]) :
            for j in range(HU.shape[1]) :
                # 差の2乗の総和
                # dif += pow(Y[i, j] - HU[i, j], 2) #べき乗の計算
                dif += (cY[i, j] - cHU[i, j]) ** 2
        return dif
    
# non-negative matrix factorization with minimization of frobenious norm
def nmf_frobenius(Y, H, U, nIter):
    row,col = Y.shape
    nBase = len(H[0,:])
    for it in range(nIter):
        
        cost = difcost_by_frobenius(Y, np.dot(H, U))
        
        print it, cost
        hnumer = np.dot(Y, U.T)
        hdenom = np.dot(np.dot(H, U), U.T)
        unumer = np.dot(H.T, Y)
        udenom = np.dot(np.dot(H.T, H), U)
        for w in range(row):
            for k in range(nBase):
                if hdenom[w,k] != 0:
                    H[w,k] = H[w,k] * hnumer[w,k] / hdenom[w,k]
        for k in range(nBase):
            for t in range(col):
                if udenom[k,t] != 0:
                    U[k,t] = U[k,t] * unumer[k,t] / udenom[k,t]

# initialization for H and U with random value within (0,1]
def init(row, col, k):
    H = np.random.random_sample(row*k).reshape(row,k)
    U = np.random.random_sample(k*col).reshape(k,col)
    return H,U

if __name__ == '__main__':
    wf = wave.open("../audioDatas/guitar.wav", "rb")
    data = wf.readframes(wf.getnframes())
    data = frombuffer(data, dtype="int16")
    N = 512
    hamming = np.hamming(N)

    # compute and show spectrogram for input signal
    figure(1)
    suptitle('Spectrogram')
    xlabel('time [sec]')
    ylabel('freqency [Hz]')
    Y,freqs,bins,im = specgram(data, NFFT=N, Fs=wf.getframerate(), noverlap=0, window=hamming)
    savefig('specgram.png',format='png')

    # parameter for non-negative matrix factorization
    # the number of basis
    nBase = 15
    nIter = 2000
    
    row,col = Y.shape
    H, U = init(row, col, nBase)
    nmf_frobenius(Y, H, U, nIter)

    # show H and U
    figure(2)
    suptitle('H (left) and U (right)')
    count = 1
    for i in range(nBase-1):
        a = subplot(nBase,2,count)
        a.tick_params(labelleft='off',labelbottom='off')
        plot(freqs,H[:,i])
        b = subplot(nBase,2,count+1)
        b.tick_params(labelleft='off',labelbottom='off')        
        plot(bins,U[i,:])
        count += 2

    a = subplot(nBase,2,count)
    a.tick_params(labelleft='off')
    plot(freqs,H[:,i])
    xlabel('freqency [Hz]')
    b = subplot(nBase,2,count+1)
    b.tick_params(labelleft='off')        
    plot(bins,U[i,:])
    xlabel('time [sec]')        
    savefig('result.png',format='png')

    show()