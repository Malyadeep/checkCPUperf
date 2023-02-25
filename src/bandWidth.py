import numba
import time
import numpy as np

from src import make_data


@numba.njit
def axpb(y, x, a, b):
    for i in range(y.shape[0]):
        y[i] = a[i] + b[i]*x[i]


def bandWidthCompute(sMin, sMax, N, base, force):
    totalInitialTime = time.perf_counter()
    print('\n\nRunning bandwidth computation....')
    try:
        data = np.load('output/data/bw_N.npz')
        if force is False:
            print('\nPrevious result found --> output/data/bw_N.npz\n')
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
        y, x, a, b = make_data.make_data(10)
        print('\n-------------------- bandWidth vs N --------------------\
              \n')
        for itr in range(sizes.shape[0]):
            y, x, a, b = make_data.make_data(sizes[itr])
            runTimeTemp = []
            initialTime = time.perf_counter()
            axpb(y, x, a, b)
            runTime1 = time.perf_counter() - initialTime
            runTimeTemp.append(runTime1)
            delta = 0.2
            for i in range(7):
                y, x, a, b = make_data.make_data(sizes[itr])
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
        np.savez('output/data/bw_N.npz', bandWidth=bandWidth, sizes=sizes)

    totalRunTime = time.perf_counter() - totalInitialTime
    print('\nBandwidth computation completed --> run time = ' +
          "{:.4e}".format(totalRunTime) + ' --> peak bandwidth = ' +
          "{:.4f}".format(np.max(bandWidth)/10**9) + ' GB/s \n')
    print('\n##############################################################' +
          '#########\n')
    return sizes, bandWidth
