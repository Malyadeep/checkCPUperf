import numpy as np
import numba
import matplotlib.pyplot as plt
import time
import flopFunc


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


def bandWidthCompute():
    try:
        data = np.load('bw_N.npz')
        sizes = data['sizes']
        bandWidth = data['bandWidth']

    except FileNotFoundError:
        print('\nFile not found: running performance test for (bandWidth\
             vs N)\n')
        sMin = 1
        sMax = 8
        N = 25
        base = 11
        sizes = np.logspace(sMin, sMax, N, base=base, dtype=int)
        bandWidth = np.zeros_like(sizes)
        print(sizes)
        y, x, a, b = make_data(10)
        print('\n\n-------------------- bandWidth vs N --------------------\n\
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
            print(sizes[itr], ', ', runTime, ', ', nLoop)
        np.savez('bw_N.npz', bandWidth=bandWidth, sizes=sizes)

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
    plt.savefig('bandwidth_vs_N.png')


def flopsCompute():
    try:
        data = np.load('flops_N.npz')
        sizes = data['sizes']
        flops = data['flops']
    except FileNotFoundError:
        print('\nFile not found: running performance test for (flops vs N)\n')
        sMin = 1
        sMax = 8
        N = 25
        base = 11
        sizes = np.logspace(sMin, sMax, N, base=base, dtype=int)
        flops = np.zeros((sizes.shape[0], 7))
        print(sizes)
        for j in range(7):
            print('\n\n-------------------- flops vs N ('+str(j)+')'
                  '--------------------\n\n')
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
                print(sizes[itr], ', ', runTime, ', ', nLoop)
        np.savez('flops_N.npz', flops=flops, sizes=sizes)

    label = ['2 flop', '4 flop', '8 flop', '16 flop', '24 flop', '32 flop',
             '64 flop']

    plt.figure(2)
    for j in range(7):
        plt.loglog(sizes, flops[:, j], marker='o', label=label[j])
    plt.legend(loc='best')
    plt.xlabel('size')
    plt.ylabel('FLOPS')
    plt.savefig('flops_vs_N.png')


if __name__ == '__main__':
    bandWidthCompute()
    flopsCompute()
