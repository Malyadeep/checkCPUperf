# checkCPUperf
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
> cd checkCPUperf/ 

and run the following command

> python -m compileall -l . src/ 

to generate the cache files. This will allow higher performance of the library from the first run itself.

With this the library is all set to go. Just run the script _performance.py_ with argument _-p_ and check the results in the _output/_ directory.
The script can be run from terminal/shell as follows
> python3 performance.py -p

The details of the results and the arguments that can be provided to the script are given in the next section.

## Usage 
The code generates arrays of various sizes and performs some computations and measures the time taken to do so. From the memory used and the floating point operations done, it calculates the peak memory bandwidth and FLOPS. The sizes of arrays are evenly spaced on a logspace and is decided by _numpy.logspace()_ function. The main script takes in arguments that specify the various arguments of the _numpy.logspace()_ function.
The main script _performance.py_ which takes the following command line arguments to manipulate array sizes
- _sMin_ -- denotes the minimum order of the array size. Default is 1.
- _sMax_ -- denotes the maximum order of the array size. Default is 8.
- _base_ -- specifies the base of the logarithm to use to generate the list of array sizes. Default is 10.
- _n_ -- number of arrays to create <br>

The code also takes following optional arguments 
- _f_ -- forces the code to run the test again and overwrite previous results if present. By default the program will not run again if previous results are present.
- _p_ -- Specifies whether to plot the data or not. Default is false. <br>

A sample run to generate arrays with specified sizes is given below
> python3 performance.py --sMin 1 --sMax 9 -n 10 --base 11 

Array sizes on which computations will be carried for given arguments:
> [11         92        781       6583      55478     467524    3939916   33202393  279802621 2357947691]
    
It should be noted that each element of the array is a _numpy.float64_ having a size of _8 bytes_. <br>

The code has 7 functions that do 2, 4, 8, 16, 24, 32 and 64 floating point opeartions multiplied by the size of the array passed. <br>

A function to plot the data is provided which can be modified to generate various linestyles and formatting. In a later release a provision could be provided that the function reads the parameters from a file.<br>
The plots also compare the peak memory bandwidth with the cache sizes of the CPU cores. The cache information can be provided in the file _cacheDetails.md_. (To find the cache details and distribution of memory, obtain a specification sheet of the CPU). __Note__ : _Make sure the largest array size exceeds the maximum cache size of the CPU to get maximum understanding from the plots_. <br>

## Best practices
- For best reults close all other applications that might be running before running the code.
- Also it is recommended that if using laptop, it is connected to AC power source.
- The machine should be set to peak performance mode for best results. In Windows and macOS, set the _performance_ mode instead of _efficiency_. In LINUX, set the _governor_ to performance.
- To ensure the code is run on a specified CPU core, the _taskset_ command can be used in LINUX. For example :
    > taskset -c [cpu_core] python3 performance.py [arguments] 

    where [cpu_core] denotes the index of the CPU cores available. (Usually starts from 0)

## Sample Results
Some sample results with explanations are provided in _SampleResults/_

Happy computing!!





