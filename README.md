# CPUperf
A simple python library to estimate the single core memory bandwidth and peak FLOPS for a given CPU

## Installation and pre-requisites
The dependencies required to run the program can be installed via following commands:
> pip install numpy <br>
> pip install numba <br>

To plot the results the program uses matplotlib library which can be installed as:
> pip install matplotlib

After the pre-requisites are installed, the library can be obtained from the repository using:
> curl -L -O https://github.com/Malyadeep/checkCPUperf/archive/main.zip  <br>
> unzip main.zip <br>
> mv checkCPUperf-main checkCPUperf  <br>

One can also directly download the tar ball or .zip file from the repository by clicking on 'code'.

After the file has been extracted go into the main folder (assuming it is checkCPUperf) using
> cd checkCPUperf/ <br>
and run the following command
> python -m compileall -l . src/ <br>
to generate the cache files. This will allow higher performance of the library from the first run itself.

With this the library is all set to go. Just run the script 'performance.py' with argument '-p' and check the results in the 'output' directory.
The script can be run from terminal/shell as follows
> python performance.py -p

The details of the results and the arguments that can be provided to the script is given in the next section.


