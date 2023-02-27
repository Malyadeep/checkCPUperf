import matplotlib.pyplot as plt
import numpy as np


def plotBandWidth(sizes, bandWidth, cache, cacheLabel):
    print('\nPlotting bandwidth....', flush=True)

    cpu_y = np.logspace(7, 12, 10, dtype=int)
    cacheKeyList = list(cache.keys())
    cacheLabelKeyList = list(cacheLabel.keys())

    plt.figure(1)
    plt.loglog(sizes, bandWidth, marker='o', base=10)
    plt.loglog(cache[cacheKeyList[0]], cpu_y, label=cacheLabelKeyList[0] +
               ':' + cacheLabel[cacheLabelKeyList[0]], base=10)
    plt.loglog(cache[cacheKeyList[1]], cpu_y, label=cacheLabelKeyList[1] +
               ':' + cacheLabel[cacheLabelKeyList[1]], base=10)
    plt.loglog(cache[cacheKeyList[2]], cpu_y, label=cacheLabelKeyList[2] +
               ':' + cacheLabel[cacheLabelKeyList[2]], base=10)
    if np.min(cache['L3']) > 0:
        plt.loglog(cache[cacheKeyList[3]], cpu_y, label=cacheLabelKeyList[3] +
                   ':' + cacheLabel[cacheLabelKeyList[3]], base=10)
    plt.legend(loc='best')
    plt.xlabel('array size')
    plt.ylabel('Memory bandwidth (bytes/sec)')
    plt.savefig('output/figures/bandwidth_vs_N.png')
    print('Finished plotting!\n', flush=True)


def plotFlops(sizes, flops):
    print('\nPlotting FLOPS....', flush=True)
    label = ['2 flop', '4 flop', '8 flop', '16 flop', '24 flop', '32 flop',
             '64 flop']

    plt.figure(2)
    for j in range(flops.shape[1]):
        plt.loglog(sizes, flops[:, j], marker='o', label=label[j], base=10)
    plt.legend(loc='best')
    plt.xlabel('array size')
    plt.ylabel('FLOPS')
    plt.xlim([np.min(sizes)-5, 5*np.max(sizes)])
    plt.savefig('output/figures/flops_vs_N.png')
    print('Finished plotting!\n', flush=True)


if __name__ == '__main__':
    print('module containing functions to plot the data')
