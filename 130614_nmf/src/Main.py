from MyWav import *
from MySineWave import *
from Nmf import *
import numpy as np

import pylab as plt

if __name__ == "__main__":
    mys = MySineWave()
    nmf = Nmf()
    myw = MyWav("../audioDatas/guitar.wav")
    
    myw.printWaveInfo()
    myw.plotSpecgram()
    
    nBase = 20
    iter = 2000
    H, U = nmf.createRandomMatrix_matrix(myw.Y, nBase)
    rH, rU = nmf.factorize_by_frobenius(myw.Y, H, U, iter)
    print myw.freqs.shape, rU.shape
    nmf.plot_HU(myw.freqs, myw.bins, rH, rU)
    myw.showPlot()