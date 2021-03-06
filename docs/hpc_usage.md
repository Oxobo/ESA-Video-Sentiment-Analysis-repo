# HPC usage

This file contains instructions for login, configuring, and using the university HPC servers to train DL models using GPUs.
More information about the HPC server is available here: https://hpcwiki.tue.nl/wiki/Main_Page

## Log into server
Connect via ssh

```ssh [username]@hpc.win.tue.nl```

## Load Anaconda
The server contains a list of modules available for usage. In our experiments, we want to use anaconda to create and manage virtual environments. The commands below can be used to load the anaconda module.

See what modules are loaded in the current session

```module list```

See the available modules that can be loaded

```module avail```

Load the anaconda module

```module load anaconda/[version]```


## Create virtual environment
Once the anaconda module is loaded, we can create a virtual environment with the following steps.

Create virtual environment for a specific Python version (3.7)

``` conda create -n [env-name] python=3.7```

Verify that the virtual enviroment was created

``` conda info --envs ```

Activate the virtual environment

``` conda activate [env-name] ```

Optional, check the Python version inside the virtual environment

## Install libraries
With a virtual environment activated, we can install the libraries required for our project.

First, add conda-forge channel to anaaconda in order to install libraries supported by the Python community, but not by anaconda

``` conda config --append channels conda-forge ```

Verify that conda-forge was added to the channels

``` conda config -- show channels ```

Install the libraries in requirements.txt

``` conda install --file requirements.txt ```

In case some libraries need to be installed manually, execute

``` conda install [library-name] ```

*Note:* this library name corresponds to the one recognized by anaconda, which is not necessarily the same used pip.

## Execute Python scripts using GPUs

* First add the following lines to the top of such script.

```
#!/usr/bin/env python

#SBATCH --partition=mcs.gpu.q
#SBATCH --output=results.out
```

The first line allows the usage of the Python interpreter defined in the anaconda virtual environment. The second line says we can use the GPUs allowed for the computer science department (mcs). The thir line defines the log file used to store the output messages generated by the Python script.

* Then, execute the script as follows

``` sbatch script.py```

* Next, see the status of your script

``` squeue -u $(whoami)```

* Finally, monitor the progress of your script

``` tail -f results.out ```
