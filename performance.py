import time
from argparse import ArgumentParser
import os

import bandWidth
import flops
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
    args = parser.parse_args()
    if not os.path.exists('output'):
        os.makedirs('output')
    bandWidthResult = bandWidth.bandWidthCompute(args.sMin, args.sMax,
                                                 args.no_of_arrays,
                                                 args.base, args.force)
    flopsResult = flops.flopsCompute(args.sMin, args.sMax, args.no_of_arrays,
                                     args.base, args.force)

    plotFunc.plotBandWidth(bandWidthResult[0], bandWidthResult[1])
    plotFunc.plotFlops(flopsResult[0], flopsResult[1])

    print('Run completed --> run time = ' + "{:.4e}".format(time.perf_counter()
          - startTime) + '\n')


if __name__ == '__main__':
    main()
