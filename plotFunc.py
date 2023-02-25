import matplotlib.pyplot as plt
import numpy as np


def plotBandWidth(sizes, bandWidth):
    print('\nPlotting bandwidth....')
    print('Reading cacheDetails.md....')
    cpuFile = open('cacheDetails.md', 'r')
    lineList = cpuFile.readlines()
    cache = {}
    cacheLabel = {}
    for itr in range(4, len(lineList)):
        temp = lineList[itr].split()
        if temp[2].lower() == 'kb':
            cache[temp[0]] = np.full((10,), fill_value=float(temp[1])*1024/8)
            cacheLabel[temp[0]] = temp[1]+' kB'
        elif temp[2].lower() == 'mb':
            cache[temp[0]] = np.full((10,), fill_value=float(temp[1]) * 1024 *
                                     1024/8)
            cacheLabel[temp[0]] = temp[1]+' MB'

    cpu_y = np.logspace(7, 12, 10, dtype=int)
    cacheKeyList = list(cache.keys())
    cacheLabelKeyList = list(cacheLabel.keys())

    plt.figure(1)
    plt.loglog(sizes, bandWidth, marker='o')
    plt.loglog(cache[cacheKeyList[0]], cpu_y, label=cacheLabelKeyList[0] +
               ':' + cacheLabel[cacheLabelKeyList[0]])
    plt.loglog(cache[cacheKeyList[1]], cpu_y, label=cacheLabelKeyList[1] +
               ':' + cacheLabel[cacheLabelKeyList[1]])
    plt.loglog(cache[cacheKeyList[2]], cpu_y, label=cacheLabelKeyList[2] +
               ':' + cacheLabel[cacheLabelKeyList[2]])
    if np.min(cache['L3']) > 0:
        plt.loglog(cache[cacheKeyList[3]], cpu_y, label=cacheLabelKeyList[3] +
                   ':' + cacheLabel[cacheLabelKeyList[3]])
    plt.legend(loc='best')
    plt.xlabel('size')
    plt.ylabel('Memory bandwidth (bytes/sec)')
    plt.savefig('output/bandwidth_vs_N.png')
    print('Finished plotting!\n')


def plotFlops(sizes, flops):
    print('\nPlotting FLOPS....')
    label = ['2 flop', '4 flop', '8 flop', '16 flop', '24 flop', '32 flop',
             '64 flop']

    plt.figure(2)
    for j in range(flops.shape[1]):
        plt.loglog(sizes, flops[:, j], marker='o', label=label[j])
    plt.legend(loc='best')
    plt.xlabel('size')
    plt.ylabel('FLOPS')
    plt.savefig('output/flops_vs_N.png')
    print('Finished plotting!\n')


if __name__ == '__main__':
    print('module containing functions to plot the data')
