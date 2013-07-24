#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
130621
Hを横長(row, nBase)
Uを縦長(nBase, col)
に変更



'''
import numpy as np
import pylab as plt
import copy
import sys
import math
import time

class Nmf:
    def __init__ (self):
        print "Nmf_init"
    
    # 特徴と重みの行列をランダムな値で初期化    
    def createRandomMatrix_array(self, Y, nBase):
        row, col = Y.shape  # Y行列の行と列をshapeメソッドを使って取得
        H = np.random.random_sample(row * nBase).reshape(row, nBase)  # 横長の基底ベクトル
        U = np.random.random_sample(nBase * col).reshape(nBase, col)  # 縦長の重みベクトル   
        return H, U
    
    def createRandomMatrix_matrix(self, Y, nBase):
        row, col = Y.shape
        H = np.matrix([[np.random.random_sample() for i in range(nBase)]for j in range(row)])  # 縦長の基底ベクトル
        U = np.matrix([[np.random.random_sample() for i in range(col)]for j in range(nBase)])  # 横長の重みベクトル
        print H.shape
        print U.shape
        return H, U
    
    # bug : 乖離度がおかしい
    def nmf_frobenius(self, Y, H, U, nIter):
        row, col = Y.shape
        nBase = len(H[0, :])
        for it in range(nIter):
            self.check_matrices(Y, H, U)            
            cost = self.difcost_by_frobenius(Y, np.dot(H, U))
            print it, cost
            hnumer = np.dot(Y, U.T)
            hdenom = np.dot(np.dot(H, U), U.T)
            unumer = np.dot(H.T, Y)
            udenom = np.dot(np.dot(H.T, H), U)
            for w in range(row):
                for k in range(nBase):
                    if hdenom[w, k] != 0:
                        H[w, k] = H[w, k] * hnumer[w, k] / hdenom[w, k]
            for k in range(nBase):
                for t in range(col):
                    if udenom[k, t] != 0:
                        U[k, t] = U[k, t] * unumer[k, t] / udenom[k, t]
    
    def difcost_by_frobenius (self, Y, HU) :
        dif = 0
        
        #M1 = np.matrix(Y)
        #M2 = np.matrix(HU)
        # 行列のすべての行をループ
        for i in range(Y.shape[0]) :
            for j in range(HU.shape[1]) :
                # 差の2乗の総和
                # dif += pow(Y[i, j] - HU[i, j], 2) #べき乗の計算
                dif += (Y[i, j] - HU[i, j]) ** 2
        return dif
    
    def difcost_by_ID(self, Y, HU):
        dif = 0
        
        for i in range(Y.shape[0]):
            for j in range(HU.shape[1]):
                dif += Y[i, j] * math.log10(Y[i, j] / HU[i, j]) - (Y[i, j] - HU[i, j])
        return dif
    
    def factorize_by_frobenius(self, Y, H, U, iter):
        startTime = time.clock()
        row, col = Y.shape
        Y = np.matrix(Y)
        
        nBase = self.assign_nBase(H=H, U=U)
        if nBase == None : sys.exit()
        
        rH = copy.deepcopy(H)
        rU = copy.deepcopy(U)
        
        
        for it in range(iter):
            HU = rH * rU  # HとUが逆になること注意
            cost = self.difcost_by_frobenius(Y, HU)
            print it, cost
            
            # 特徴の行列を更新
            Hnumer = (Y * rU.T)
            Hdenom = (rH * rU * rU.T)
            #self.print_matrices(rH, Hnumer, Hdenom)
            # 更新
            rH = np.matrix(np.array(rH) * np.array(Hnumer) / np.array(Hdenom))
            
            # 重みの行列を更新
            Unumer = (rH.T * Y)
            Udenom = (rH.T * rH * rU)
            #self.print_matrices(rU, Unumer, Udenom)
            
            # 更新
            rU = np.matrix (np.array(rU) * np.array(Unumer) / np.array(Udenom))
            
        # print rH.shape, rU.shape
        endTime = time.clock()
        print endTime - startTime
        return rH, rU  
    
    
    
    def for_factorize_by_frobenius(self, Y, H, U, iter):
        startTime = time.clock()
        row, col = Y.shape
        #Y = np.array(Y)
        #H = np.array(H)
        #U = np.array(U)
        
        nBase = self.assign_nBase(H=H, U=U)
        if nBase == None : sys.exit()
        
        rH = copy.deepcopy(H)
        rU = copy.deepcopy(U)
        
        
        for it in range(iter):
            HU = np.dot(rH, rU)
            cost = self.difcost_by_frobenius(Y, HU)
            print it, cost
            
            Xkn = self.calc_dot(M1=rH, M2=rU)
            
            # 特徴の行列を更新
#             Hnumer = (rU.T * Y)
#             Hdenom = (rU.T * rU * rH)
            Hn = self.calc_dot(M1=Y, M2=rU.T)
            Hd = self.calc_dot(M1=Xkn, M2=rU.T)
            #self.print_matrices(rH, Hn, Hd)
            # 更新
            rH = np.matrix(np.array(rH) * np.array(Hn) / np.array(Hd))
            #rH = np.array(rH)
            
            # 重みの行列を更新
            Un = self.calc_dot(M1=rH.T, M2=Y)
            hoge = self.calc_dot(M1=rH.T, M2=rH)
            Ud = self.calc_dot(hoge, rU)
            #self.print_matrices(rU, Un, Ud)
            # 更新
            rU = np.matrix (np.array(rU) * np.array(Un) / np.array(Ud))
            #rU = np.array(rU)
            
            
        # print rH.shape, rU.shape
        endTime = time.clock()
        print endTime - startTime
        return rH, rU  
    
    
    def test_factorize_by_frobenius(self, Y, H, U, iter):
        row, col = Y.shape
        Y = np.matrix(Y)
        
        nBase = self.assign_nBase(H=H, U=U)
        if nBase == None : sys.exit()
        
        rH = copy.deepcopy(H)
        rU = copy.deepcopy(U)
        
        
        for it in range(iter):
            HU = rH * rU  # HとUが逆になること注意
            cost = self.difcost_by_frobenius(Y, HU)
            print it, cost
            
            X = np.dot(rH, rU)
            # 特徴の行列を更新
            Hnumer = np.zeros([row, col])
            for k in range(row):
                for n in range(col):
                    for m in range(nBase):
                        Hnumer += Y[k, n] * rU[m, n]
            Hdenom = np.zeros([k, m])
            for k in range(row):
                for n in range(col):
                    for m in range(nBase):
                        Hdenom += rH[k, m] * rU[m, n] * rU[m, n]
        
            self.print_matrices(rH, Hnumer, Hdenom)
            # 更新
            for k in range(row):
                for m in range(nBase):
                    if Hdenom[k, m] != 0:
                        rH[k, m] = rH[k, m] * Hnumer[k, m] / Hdenom[k, m]
                    
            
            # 重みの行列を更新
            Unumer = (rH.T * Y)
            Udenom = (rH.T * rH * rU)
            #self.print_matrices(rU, Unumer, Udenom)
            
            # 更新
            rU = np.matrix (np.array(rU) * np.array(Unumer) / np.array(Udenom))
            
        # print rH.shape, rU.shape
        endTime = time.clock()
        print endTime - startTime
        return rH, rU  
    def calc_dot(self, M1, M2):
        row = M1.shape[0]
        col = M2.shape[1]
        
        if M1.shape[1] == M2.shape[0]:
            nBase = M1.shape[1]
            ans = np.zeros([row, col])
            for i in range(row):
                for j in range(col):
                    for k in range(nBase):
                        ans[i,j] += M1[i, k] * M2[k, j]
            return ans
                        
        else:
            print "can_not_calc"
        
    def factorize_by_ID (self, Y, H, U, iter):
        row, col = Y.shape
        
        
        nBase = self.assign_nBase(H=H, U=U)
        if nBase == None : sys.exit()
        
        rH = copy.deepcopy(H)
        rU = copy.deepcopy(U)
        
        #self.check_matrices(M1=Y, M2=H, M3=U)
        
        for it in range(iter):
            HU = np.dot(rH, rU)
            cost = self.difcost_by_frobenius(Y, HU)
            print it, cost
            
            
            # 特徴の行列を更新
            r = Y.shape[0]
            c = rU.T.shape[1]
            b = Y.shape[1]
            
            Xkn = np.dot(rH, rU)
            Hnumer = np.zeros([r, c])
            Hdenom = np.zeros([r, c])
            for i in range(r):
                for j in range(c):
                    for k in range(b):
                        Hnumer += (Y[i, k] * rU.T[k, j]) / Xkn[i, k]
            
            for i in range(row):
                for j in range(col):
                    Hdenom += rU.T[i, j]
            
            print self.print_matrices(rH, Hnumer, Hdenom)
            # 更新
            rH = np.matrix(np.array(rH) * np.array(Hnumer) / np.array(Hdenom))
            
            # 重みの行列を更新
            r = rH.T.shape[0]
            c = Y.shape[1]
            b = Y.shape[0]
            
            Unumer = np.zeros([r,c])
            Hdenom = np.zeros([r,c])
            self.print_matrices(rH.T, Y, Xkn)
            print r, c, b
            for i in range(r):
                for j in range(c):
                    for k in range(b):
                        Unumer += (rH.T[i, k] * Y[k, j]) / Xkn[j, k]
            
            for i in range(row):
                for j in range(col):
                    Udenom += rH.T[i, j]
            
            
            # 更新
            rU = np.matrix (np.array(rU) * np.array(Unumer) / np.array(Udenom))
            
        # print rH.shape, rU.shape
        return rH, rU  
    
    def assign_nBase(self, H, U):
        nBase = None
        # Hの列数とUの行数一致したときのnBaseに代入
        if H.shape[1] == U.shape[0] : 
            nBase = H.shape[1]
            print "nBase_was_assigned"
        else :
            print "nBase_Error"
        return nBase
    
    def print_matrices(self, M1, M2, M3):
        
        MsList = [M1, M2, M3]
        MsNList = ['M1', 'M2', 'M3']
        
        for i in range(len(MsList)):
            print MsNList[i], np.array(MsList[i]).shape
        
        
    def plot_HU(self, freqs, bins, H, U):
        # H, Uの表示
        plt.figure(2)
        plt.suptitle('H (left) and U (right)')
        count = 1
        
        # plotするためにnp.array型に変換
        H = np.array(H)
        U = np.array(U)
        
        nBase = self.assign_nBase(H=H, U=U)
        if nBase == None : sys.exit()
        for i in range(nBase - 1) :
            a = plt.subplot(nBase, 2, count)
            a.tick_params(labelleft='off', labelbottom='off')
            plt.plot(freqs, H[:, i])
            b = plt.subplot(nBase, 2, count + 1)
            b.tick_params(labelleft='off', labelbottom='off')
            plt.plot(bins, U[i, :])
            count += 2
    
        a = plt.subplot(nBase, 2, count)
        a.tick_params(labelleft='off')
        plt.plot(freqs, H[:, i])
        plt.xlabel('freqency [Hz]')
        b = plt.subplot(nBase, 2, count + 1)
        b.tick_params(labelleft='off')        
        plt.plot(bins, U[i, :])
        plt.xlabel('time [sec]')        
        plt.savefig('../picDatas/result.png', format='png')
        #plt.show()
        
#         def testPlot_HU(self, freqs, bins, H, U):
#             # H, Uの表示
#             plt.figure(2)
#             plt.suptitle('H (left) and U (right)')
#             count = 1
#             
#             # plotするためにnp.array型に変換
#             H = np.array(H)
#             U = np.array(U)
#             
#             nBase = self.assign_nBase(H=H, U=U)
#             if nBase == None : sys.exit()
#             for i in range(nBase - 1) :
#                 a = plt.subplot(nBase, 2, count)
#                 a.tick_params(labelleft='off', labelbottom='off')
#                 plt.plot(freqs, U[:, i])
#                 b = plt.subplot(nBase, 2, count + 1)
#                 b.tick_params(labelleft='off', labelbottom='off')
#                 plt.plot(bins, H[i, :])
#                 count += 2
#         
#             a = plt.subplot(nBase, 2, count)
#             a.tick_params(labelleft='off')
#             plt.plot(freqs, U[:, i])
#             plt.xlabel('freqency [Hz]')
#             b = plt.subplot(nBase, 2, count + 1)
#             b.tick_params(labelleft='off')        
#             plt.plot(bins, H[i, :])
#             plt.xlabel('time [sec]')        
#             plt.savefig('../picDatas/result.png', format='png')

if __name__ == "__main__" :
    nmf = Nmf()
    
    Y = np.random.random_sample (3 * 4).reshape(3, 4)
    # print Y
    nBase = 6
    iter = 1000
    H, U = nmf.createRandomMatrix_matrix(Y, nBase)
      
    #print nmf.difcost_by_ID(Y, U * H)
    
    #nmf.for_factorize_by_frobenius(Y, H, U, iter)
    #print "cccccccccccccccccccc"
    #nmf.factorize_by_ID(Y, H, U, iter)
    #nmf.check_matrices(M1=Y, M2=H, M3=U)
    nmf.test_factorize_by_frobenius(Y, H, U, iter)
    #H, U = nmf.createRandomMatrix_array(Y, nBase)
    #nmf.nmf_frobenius(Y, H, U, iter)
    
    X = np.arange(12).reshape(3, 4)
    Y = np.arange(12).reshape(4, 3)

#     print nmf.calc_dot(X, Y)
#     print np.dot(X, Y)