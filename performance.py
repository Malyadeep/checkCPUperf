import time
from argparse import ArgumentParser
import os
import numpy as np

from src import bandWidth, flops
import plotFunc


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
    parser.add_argument('-p', '--plot', action='store_true', default=False,
                        help='if selected plots the results')
    args = parser.parse_args()
    if not os.path.exists('output'):
        print("\n'output/' not present : Creating 'output/'\n", flush=True)
        os.makedirs('output')
        os.makedirs('output/data')
        os.makedirs('output/figures')
    else:
        print("'output/' exists\n", flush=True)
        if not os.path.exists('output/data'):
            os.makedirs('output/data')
            if args.plot is True and not os.path.exists('output/figures'):
                os.makedirs('output/figures')
    print('################### Input parameters ###################',
          flush=True)
    print('--> sMin = '+str(args.sMin), flush=True)
    print('--> sMax = '+str(args.sMax), flush=True)
    print('--> no.of arrays = '+str(args.no_of_arrays), flush=True)
    print('--> base = '+str(args.base), flush=True)
    print('--> plot results = '+str(args.plot), flush=True)
    print('#########################################################',
          flush=True)
    print('Reading cacheDetails.md....', flush=True)
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
    print('#########################################################',
          flush=True)

    bandWidthResult = bandWidth.bandWidthCompute(args.sMin, args.sMax,
                                                 args.no_of_arrays,
                                                 args.base, args.force)
    flopsResult = flops.flopsCompute(args.sMin, args.sMax, args.no_of_arrays,
                                     args.base, args.force, cache, cacheLabel)

    if args.plot is True:
        plotFunc.plotBandWidth(bandWidthResult[0], bandWidthResult[1],
                               cache, cacheLabel)
        plotFunc.plotFlops(flopsResult[0], flopsResult[1])
    else:
        print('Plot option not selected --> Results not plotted', flush=True)

    print('Run completed --> run time = ' + "{:.4e}".format(time.perf_counter()
          - startTime) + '\n', flush=True)


if __name__ == '__main__':
    main()
