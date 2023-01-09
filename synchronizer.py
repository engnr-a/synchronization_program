"""File Synchronization Program

This is the main program file. The program takes four arguments from the command line. The arguments validated using the imported validator function.
It then defines various variables from the validated command line arguments. Source and replica paths are compared using the directory comparison
instance. File operations related to synchronization of the source and replica path are carried out and logged using imported file handling function. 
The program requires the installation of schedule. This can either be done using this module or installed via the command line using pip command.

@param source_path_argument: This is the source path where all files to the synchronized are held.
@param replica_path_argument: This is the backup path that maintains a replica copy of all files and directory in the source path.
@param sync_interval_argument: The synchronization interval in seconds. 
@param log_path_argument: The directory to which to write the synchronization related logs. The programs provides the log file name from the log path.
"""

import sys
import os
from filecmp import dircmp
import time
import logging
import subprocess
import traceback

from utilityfunctions import cmd_argument_validator 
from utilityfunctions import file_handler 

# Install schedule
# Perhaps it would have been better to use "shed" instead of installing schedule. However, I personally prefer schedule.
# I also understand that install call within the python module might not be desirable from different perspective.
try:
    import schedule
except ModuleNotFoundError:
    logging.debug("Unable to import scheule module. Will try to install it.")
    python = sys.executable
    try:
        subprocess.check_call([python, '-m', 'pip', 'install', 'schedule'])
    except Exception as thrown_exception:
           logging.debug( "Some error or exception encountered while trying to install schedule. If this persist, try using pip command to install the module")  
           logging.debug( "Some details:\n {} \n {}".format(thrown_exception,traceback.format_exc()) ) 


# A list holding the passed command line arguments
cmd_arguments_list = list(sys.argv)

#print(type(cmd_arguments_list))

# Validate the command line arguments using the function from utilityfuncions module
cmd_argument_validator(cmd_arguments_list)

# Variables definitions using the validated command line arguments
source_path_argument = cmd_arguments_list[1]  
replica_path_argument = cmd_arguments_list[2]
sync_interval_argument = cmd_arguments_list[3]  
log_path_argument = cmd_arguments_list[4]   
 

def synchnozation_job():
    """File synchronization function. 

    This function uses the directory comparison instance along with the file_handler function to perform various file/path
    handling operations related to synchronization between the source and replica paths.
    """

    # Directory comparison instance
    dcmp = dircmp(source_path_argument, replica_path_argument)
    
    # Define the log file using the provided log path
    user_log_file = log_path_argument + "\\" + "synclogs.log"

    # Path object casting for safety
    log_file = os.path.normpath((r'%s' % user_log_file))

    # Use the file_handler function from utilityfuncions module to perform various file operations based on paths comparisons
    file_handler(dcmp, log_file)
    

# Define the schedule attribute using the syn
schedule.every(int(sync_interval_argument)).seconds.do(synchnozation_job)

# Schedule task checker with while loop
while True:
    schedule.run_pending()
    time.sleep(1)