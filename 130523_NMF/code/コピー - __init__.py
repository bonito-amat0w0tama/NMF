#/usr/bin/python2.7
# -*_ coding: utf-8 -*-

import numpy as np

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
def factorrize (v, pc = 10, iter = 50) :
    ic, fc = v.shape #shape関数で行列の行と列の取得
    
    #特徴と重みの行列をランダムな値で初期化
    #列→行の順番でランダムな値で行列を生成
    w = np.matrix ([[np.random.random_sample() for i in range(pc)] 
                    for j in range(ic)])
    h = np.matrix ([[np.random.random_sample() for i in range(fc)]
                    for i in range(pc)])
    
    #最大でiterの回数だけ操作を繰り返す
    for i in range(iter) :
        wh = w * h
        
        #現在の差の計算
        cost = difcost (v, wh)
        
        #行列が完全に因子分解されたら終了
        if cost == 0 :
            break
        
        
        #特徴の行列を更新
        
        #転置した重みの行列にデータ行列を掛け合わせたもの
        hn = (np.transpose(w) * v)
        
        #天地した重みの行列に重みの行列を掛け合わせたものに
        #特徴の行列を掛け合わせたもの
        hd = (np.transpose(w) * w * h)
        
        #更新
        h = np.matrix(np.array(h) * np.array(hn) / np.array(hd))
        
        #重みの行列を更新
        
        #データ行列に転置した特徴の行列を掛け合わせたもの
        wn = v * h.T
        
        #重みの行列に、特徴の行列を掛け合わせたものに
        #転置した特徴の行列を掛け合わせたもの
        wd = w * h * h.T
        
        #更新
        w = np.matrix (np.array(w) * np.array(wn) / np.array(wd))
    
    return w, h

if __name__ == "__main__" :
    Mat = np.random.random_sample(2 * 3).reshape(2, 3)
    
    w, h = factorrize (Mat, pc = 4, iter = 100)
    
    
    print w
    print h
    print w * h
    print Mat