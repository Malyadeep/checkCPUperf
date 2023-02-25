import time
import numpy as np

from src import make_data, flopFunc


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
                y_test, x_test, a_test, b_test = make_data.make_data(5)
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
                y, x, a, b = make_data.make_data(sizes[itr])
                runTimeTemp = []
                initialTime = time.perf_counter()
                func(y, x, a, b)
                runTime1 = time.perf_counter() - initialTime
                runTimeTemp.append(runTime1)
                delta = 0.2
                for i in range(7):
                    y, x, a, b = make_data.make_data(sizes[itr])
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

    totalRunTime = time.perf_counter() - totalInitialTime
    print('\nFLOPS computation completed --> run time = ' +
          "{:.4e}".format(totalRunTime) + ' --> peak GFLOPS = ' +
          "{:.4f}".format(np.max(flops)/10**9) + '\n')
    print('\n##############################################################' +
          '#########\n')
    return sizes, flops
