# CPUperf
A simple python library to estimate the single core memory bandwidth and peak FLOPS for a given CPU

## Installation and pre-requisites
The dependencies required to run the program can be installed via following commands:
> pip install numpy <br>
> pip install numba <br>

To plot the results the program uses _matplotlib_ library which can be installed as:
> pip install matplotlib

After the pre-requisites are installed, the library can be obtained from the repository using:
> curl -L -O https://github.com/Malyadeep/checkCPUperf/archive/main.zip  <br>
> unzip main.zip <br>
> mv checkCPUperf-main checkCPUperf  <br>

One can also directly download the tar ball or .zip file from the repository by clicking on __code__.

After the file has been extracted go into the main folder (assuming it is _checkCPUperf/_) using
> cd checkCPUperf/ <br>
and run the following command
> python -m compileall -l . src/ <br>
to generate the cache files. This will allow higher performance of the library from the first run itself.

With this the library is all set to go. Just run the script _performance.py_ with argument _-p_ and check the results in the _output/_ directory.
The script can be run from terminal/shell as follows
> python performance.py -p

The details of the results and the arguments that can be provided to the script are given in the next section.

# Usage 
The code generates arrays of various sizes and performs some computations and measures the time taken to do so. From the memory used and the floating point operations done, it calculates the peak memory bandwidth and FLOPS. The sizes of arrays are evenly spaced on a logspace and is decided by _numpy.logspace()_ function. The main script takes in arguments that specify the various arguments of the _numpy.logspace()_ function.
The main script _performance.py_ which takes the following command line arguments to manipulate array sizes
- _sMin_ -- denotes the minimum order of the array size
- _sMax_ -- denotes the maximum order of the array size
- _base_ -- specifies the base of the logarithm to use to generate the list of array sizes
- _n_ -- number of arrays to create 
The code also takes following optional arguments 
- _f_ -- forces the code to run the test again and overwrite previous results if present. By default the program will not run again if previous results are present.
- _p_ -- Specifies whether to plot the data or not. Default is false.






