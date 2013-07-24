from MyWav import *
from MySineWave import *
from Nmf import *
import numpy as np

import pylab as plt
import nimfa

if __name__ == "__main__":
    mys = MySineWave()
    nmf = Nmf()
    myw = MyWav("../audioDatas/guitar.wav")
    
    #myw.printWaveInfo()
    myw.plotSpecgram()
    
    fctr = nimfa.mf(myw.Y, method = "nmf", max_iter = 300, rank = 15, update = 'divergence', objective = 'div')
    fctr_res = nimfa.mf_run(fctr)
    
    
    W = fctr_res.basis()
    print "Basis_matrix"
    print W
    
    H = fctr_res.coef()
    print "coef"
    print H
    
    
    sm = fctr_res.summary()
    print "RSS: %8.3f" % sm["rss"]
    print "Evar: %8.3f" % sm["evar"]
    print "Iterations: %8.3f" % sm["n_iter"]
    print "Euclidean distance: %8.3f" %sm["euclidean"]
    print "sparseness, W: %5.4f, H: %5.4f" % fctr_res.fit.sparseness()
    
    print W.shape
    print H.shape
    nmf.plot_HU(myw.freqs, myw.bins, W, H)
    plt.show()
    
    #     nBase = 20
#     iter = 20
#     H, U = nmf.createRandomMatrix_matrix(myw.Y, nBase)
#     rH, rU = nmf.testFactorize_by_frobenius(myw.Y, H, U, iter)
#     #print myw.freqs.shape, rU.shape
#     nmf.plot_HU(myw.freqs, myw.bins, rH, rU)
#     myw.showPlot()