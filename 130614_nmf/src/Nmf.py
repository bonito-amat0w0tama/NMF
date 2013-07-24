#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt
import copy
import sys
import math

class Nmf:
    def __init__ (self):
        print "Nmf_init"
    
    #def factorize(self, Y, nbase, iter):
    
    #特徴と重みの行列をランダムな値で初期化    
    def createRandomMatrix_array(self, Y, nBase):
        row, col = Y.shape # Y行列の行と列をshapeメソッドを使って取得
        H = np.random.random_sample(nBase * row).reshape(nBase, row) # 縦長の基底ベクトル
        U = np.random.random_sample(col * nBase).reshape(col, nBase) # 横長の重みベクトル   
        return H, U
    
    def createRandomMatrix_matrix(self, Y, nBase):
        row, col = Y.shape
        H = np.matrix([[np.random.random_sample() for i in range(col)]for j in range(nBase)]) # 縦長の基底ベクトル
        U = np.matrix([[np.random.random_sample() for i in range(nBase)]for j in range(row)]) # 横長の重みベクトル
        print H.shape
        print U.shape
        return H, U
    
    
    def difcost_by_frobenius (self, Y, HU) :
        dif = 0
        #行列のすべての行をループ
        for i in range(Y.shape[0]) :
            for j in range(HU.shape[1]) :
                #差の2乗の総和
                #dif += pow(Y[i, j] - HU[i, j], 2) #べき乗の計算
                dif += (Y[i, j] - HU[i, j]) ** 2
        return dif
    
    def difcost_by_ID(self, Y, HU):
        dif = 0
        
        for i in range(Y.shape[0]):
            for j in range(HU.shape[1]):
                dif += Y[i, j] * math.log10(Y[i, j] / HU[i, j]) - (Y[i, j] - HU[i, j])
        return dif
    
    def factorize_by_frobenius(self, Y, H, U, iter):
        row, col = Y.shape
        Y = np.matrix(Y)
        
        # Hの行数とUの列数が一致したときのnBaseに代入
        if H.shape[0] == U.shape[1] : 
            nBase = H.shape[0]
            print "nBase_init"
        else : 
            print "nBase_Error"
            sys.exit()
        
        rH = copy.deepcopy(H)
        rU = copy.deepcopy(U)
        
        
        for it in range(iter):
            HU = rU * rH # HとUが逆になること注意
            cost = self.difcost_by_frobenius(Y, HU)
            print it, cost
            
            #特徴の行列を更新
            Hnumer = (rU.T * Y)
            Hdenom = (rU.T * rU * rH)
            
            #更新
            rH = np.matrix(np.array(rH) * np.array(Hnumer) / np.array(Hdenom))
            
            #重みの行列を更新
            Unumer = Y * rH.T
            Udenom = rU * rH * rH.T
            
            #更新
            rU = np.matrix (np.array(rU) * np.array(Unumer) / np.array(Udenom))
            
        print rH.shape, rU.shape
        return rH, rU  
    def plot_HU(self, freqs, bins, H, U):
        # H, Uの表示
        plt.figure(2)
        plt.suptitle('H (left) and U (right)')
        count = 1
        
        H = np.array(H)
        U = np.array(U)
        # Hの行数とUの列数が一致したときのnBaseに代入
        if H.shape[0] == U.shape[1] : 
            nBase = H.shape[0]
            print "nBase_init"
        else : 
            print "nBase_Error"
            sys.exit()
        
        for i in range(nBase - 1) :
            a = plt.subplot(nBase, 2, count)
            a.tick_params(labelleft='off',labelbottom='off')
            plt.plot(freqs,U[:,i])
            b = plt.subplot(nBase,2,count+1)
            b.tick_params(labelleft='off',labelbottom='off')
            plt.plot(bins, H[i,:])
            count += 2
    
        a = plt.subplot(nBase,2,count)
        a.tick_params(labelleft='off')
        plt.plot(freqs,U[:,i])
        plt.xlabel('freqency [Hz]')
        b = plt.subplot(nBase,2,count+1)
        b.tick_params(labelleft='off')        
        plt.plot(bins,H[i,:])
        plt.xlabel('time [sec]')        
        plt.savefig('../picDatas/result.png',format='png')

if __name__ == "__main__" :
    nmf = Nmf()
    
    Y = np.random.random_sample (3 * 4).reshape(3, 4)
    #print Y
    nBase = 6
    iter = 10000000
    H,U = nmf.createRandomMatrix_matrix(Y, nBase)
    
      
    print nmf.difcost_by_ID(Y, U * H)
    
    #nmf.factorize_by_frobenius(Y, H, U, iter)

    
    
    