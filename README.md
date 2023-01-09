# synchronization_program

### Python Implementation of Path Synchronization 

This repository contains python implementation of one-way synchronization of paths from source to replica/target. The program takes four command line
arguments: the source path, target/replica path, time (in seconds) interval of synchronization  and the log path.

The repository contains two core modules and one test module. The `utilityfunction` module handles command line validations and file handling operations related to
synchronization of files and directories. The `synchronizer` module combines functions from the previous module with job schedule to implement the actual task
of path synchronization

### How To Use
- Python and schedule library must be installed to use the program. 
- Schedule can be installed by correctly running the module or installed via the command line using pip: `pip install schedule`
- To run the program run the `synchronizer.py` file passing the required arguments: the source path, replica path, synchronization interval and log path in that order
`python synchronizer.py sourcepath replicapath 5 logpath `
