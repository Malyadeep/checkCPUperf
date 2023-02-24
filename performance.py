import numpy as np
import numba
import matplotlib.pyplot as plt
import time
from argparse import ArgumentParser
import flopFunc
import os


def make_data(N):
    x = np.linspace(0, 2*np.pi, N)
    a = np.linspace(0, np.pi, N)
    b = np.linspace(0, np.pi/2, N)
    y = np.zeros_like(x)
    return y, x, a, b


@numba.njit
def axpb(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = a[i] + b[i]*x[i]


def bandWidthCompute(sMin, sMax, N, base, force):
    totalInitialTime = time.perf_counter()
    try:
        data = np.load('output/bw_N.npz')
        if force is False:
            print('\nPrevious result found --> replotting the results\n')
            sizes = data['sizes']
            bandWidth = data['bandWidth']
        else:
            print('\nforce option selected --> running test again\n')
            print('WARNING! --> This will overwrite previous results')
            raise Exception
    except Exception:
        if force is False:
            print('\nNo previous results found: running performance test for' +
                  ' peak bandwidth\n')
        sizes = np.logspace(sMin, sMax, N, base=base, dtype=int)
        bandWidth = np.zeros_like(sizes)
        y, x, a, b = make_data(10)
        print('\n-------------------- bandWidth vs N --------------------\
              \n')
        for itr in range(sizes.shape[0]):
            y, x, a, b = make_data(sizes[itr])
            runTimeTemp = []
            initialTime = time.perf_counter()
            axpb(y, x, a, b)
            runTime1 = time.perf_counter() - initialTime
            runTimeTemp.append(runTime1)
            delta = 0.2
            for i in range(7):
                y, x, a, b = make_data(sizes[itr])
                nLoop = 0
                initialTime = time.perf_counter()
                while time.perf_counter() - initialTime < delta:
                    axpb(y, x, a, b)
                    nLoop += 1
                runTimeTemp.append(delta/nLoop)

            runTime = np.min(np.array(runTimeTemp))
            bandWidth[itr] = (y.nbytes + x.nbytes + a.nbytes + b.nbytes)\
                / runTime
            print(str(int(itr*100/sizes.shape[0])).ljust(2), '% done ',
                  '| array size = ', str(sizes[itr]).ljust(12),
                  '| run time = ', "{:.4e}".format(runTime),
                  '| no.of iterations = ', str(nLoop).ljust(8))
        np.savez('output/bw_N.npz', bandWidth=bandWidth, sizes=sizes)

    cpu_L1 = np.full((10,), fill_value=32*1024/8)
    cpu_L2_s = np.full((10,), fill_value=512*1024/8)
    cpu_L2_l = np.full((10,), fill_value=2*1024*1024/8)
    cpu_L3 = np.full((10,), fill_value=8*1024*1024/8)
    cpu_y = np.logspace(7, 12, 10, dtype=int)

    plt.figure(1)
    plt.loglog(sizes, bandWidth, marker='o')
    plt.loglog(cpu_L1, cpu_y, label='L1:32kB')
    plt.loglog(cpu_L2_s, cpu_y, label='L2:512kB')
    plt.loglog(cpu_L2_l, cpu_y, label='L2:6MB')
    plt.loglog(cpu_L3, cpu_y, label='L3:64MB')
    plt.legend(loc='best')
    plt.xlabel('size')
    plt.ylabel('Memory bandwidth (bytes/sec)')
    plt.savefig('output/bandwidth_vs_N.png')

    totalRunTime = time.perf_counter() - totalInitialTime
    print('\nBandwidth computation completed --> run time = ' +
          "{:.4e}".format(totalRunTime) + ' --> peak bandwidth = ' +
          "{:.4f}".format(np.max(bandWidth)/10**9) + ' GB/s \n')
    print('\n##############################################################' +
          '#########\n')


def flopsCompute(sMin, sMax, N, base, force):
    totalInitialTime = time.perf_counter()
    try:
        data = np.load('output/flops_N.npz')
        if force is False:
            print('\nPrevious result found --> replotting the results\n')
            sizes = data['sizes']
            flops = data['flops']
        else:
            print('\nforce option selected --> running test again\n')
            print('WARNING! --> This will overwrite previous results')
            raise Exception
    except Exception:
        if force is False:
            print('\nNo previous results found: running performance test for' +
                  ' peak FLOPS\n')
        sizes = np.logspace(sMin, sMax, N, base=base, dtype=int)
        flops = np.zeros((sizes.shape[0], 7))
        for j in range(7):
            print('\n-------------------- flops vs N ('+str(j+1)+'/7)' +
                  '--------------------\n')
            for itr in range(sizes.shape[0]):
                y_test, x_test, a_test, b_test = make_data(5)
                if j == 0:
                    func = flopFunc.flop2
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 2*sizes[itr]
                elif j == 1:
                    func = flopFunc.flop4
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 4*sizes[itr]
                elif j == 2:
                    func = flopFunc.flop8
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 8*sizes[itr]
                elif j == 3:
                    func = flopFunc.flop16
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 16*sizes[itr]
                elif j == 4:
                    func = flopFunc.flop24
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 24*sizes[itr]
                elif j == 5:
                    func = flopFunc.flop32
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 32*sizes[itr]
                else:
                    func = flopFunc.flop64
                    func(y_test, x_test, a_test, b_test)
                    totFlops = 64*sizes[itr]
                y, x, a, b = make_data(sizes[itr])
                runTimeTemp = []
                initialTime = time.perf_counter()
                func(y, x, a, b)
                runTime1 = time.perf_counter() - initialTime
                runTimeTemp.append(runTime1)
                delta = 0.2
                for i in range(7):
                    y, x, a, b = make_data(sizes[itr])
                    nLoop = 0
                    initialTime = time.perf_counter()
                    while time.perf_counter() - initialTime < delta:
                        func(y, x, a, b)
                        nLoop += 1
                    runTimeTemp.append(delta/nLoop)

                runTime = np.min(np.array(runTimeTemp))
                flops[itr, j] = totFlops/runTime
                print(str(int(itr*100/sizes.shape[0])).ljust(2), '% done ',
                      '| array size = ', str(sizes[itr]).ljust(12),
                      '| run time = ', "{:.4e}".format(runTime),
                      '| no.of iterations = ', str(nLoop).ljust(8))
        np.savez('output/flops_N.npz', flops=flops, sizes=sizes)

    label = ['2 flop', '4 flop', '8 flop', '16 flop', '24 flop', '32 flop',
             '64 flop']

    plt.figure(2)
    for j in range(7):
        plt.loglog(sizes, flops[:, j], marker='o', label=label[j])
    plt.legend(loc='best')
    plt.xlabel('size')
    plt.ylabel('FLOPS')
    plt.savefig('output/flops_vs_N.png')

    totalRunTime = time.perf_counter() - totalInitialTime
    print('\nFLOPS computation completed --> run time = ' +
          "{:.4e}".format(totalRunTime) + ' --> peak GFLOPS = ' +
          "{:.4f}".format(np.max(flops)/10**9) + '\n')
    print('\n##############################################################' +
          '#########\n')


def main():
    startTime = time.perf_counter()
    parser = ArgumentParser(description='Estimate peak bandwidth and GFLOPS ' +
                            'of CPU')
    parser.add_argument('--sMin', default=1, type=int,
                        help='Min. order of array size')
    parser.add_argument('--sMax', default=8, type=int,
                        help='Max. order of array size')
    parser.add_argument('--base', default=10, type=int,
                        help='base of the log-scale to generate arrays ' +
                        'of different sizes based on the minimum and ' +
                        'maximum order')
    parser.add_argument('-n', '--no_of_arrays', default=25, type=int,
                        help='no.of arrays to generate')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='force to run the test again and ' +
                        'overwrite previous results')
    args = parser.parse_args()
    if not os.path.exists('output'):
        os.makedirs('output')
    bandWidthCompute(args.sMin, args.sMax, args.no_of_arrays, args.base,
                     args.force)
    flopsCompute(args.sMin, args.sMax, args.no_of_arrays, args.base,
                 args.force)
    print('Run completed --> run time = ' + "{:.4e}".format(time.perf_counter()
          - startTime) + '\n')


if __name__ == '__main__':
    main()
