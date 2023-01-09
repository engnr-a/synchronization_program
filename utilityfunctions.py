"""File Synchronization Program

This is an utility module. It defines logging instance and uts basic configurations. It provides the two essential functions for 
command line argument validation and file handling operations.
"""
#imports
import sys
import logging
import os
from os import path
from filecmp import dircmp
import shutil
import traceback


# Logging configurations
# The logging configurations could also have been done via a config file (example using the YAML format) and replicated across modules. 
# However, I consider that as a potential overkill given the simplicity of the program and since I am only logging from a rather simple functions..

# logging instance    
customlog = logging.getLogger(__name__)
customlog.setLevel(logging.DEBUG)

# Program level logging into file. This is primarily for debugging. It is not the same as the user log. User log path will provided by user.
program_file_log = logging.FileHandler("progam_log.log")
program_file_log.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s [ %(levelname)s ] - %(message)s', datefmt="%d/%m/%Y %H:%M")
program_file_log.setFormatter(log_format)

# Logging for console
program_console_log = logging.StreamHandler()
program_console_log.setLevel(logging.DEBUG)
program_console_log.setFormatter(log_format)

# Add the file and console log to logging instance
customlog.addHandler(program_file_log)
customlog.addHandler(program_console_log)



def cmd_argument_validator(cmd_args):
    """Basic sanity check of the passed command line argument. 

    First argument is the source path, second argument is the replica path, third argument is the
    synchronization interval, while the fourth argument is the log file path. Additionally, the
    interval must be castable to positive integer data type. The source path and replica path should
    be an existing directory.
    """
    
    # try-catch code block
    # try-catch for wildcard errors/exceptions might not be the best approach (compared with catching specific exceptions/errors), 
    # However, given the pre-checks implemented, I think the pros outweigh the cons.
    try:

        # Length check of the command line arguments
        if (len(cmd_args) != 5):
            customlog.error("The program requires exactly four arguments. The source path, replica path, sync interval and log path in this order.")
            raise SystemExit
            #sys.exit()
    
        # Synchronization interval validation
        elif((cmd_args[3].isdigit() == False) or (cmd_args[3] == 0)):
            customlog.error("Synchronization interval argument should be a positive number that represents time in seconds")
            sys.exit()

        # Verify that the source path is an existing directory  
        elif((path.exists(cmd_args[1]) == False) or (path.isdir(cmd_args[1]) == False) ):
            customlog.error("Provided source path argument ({}) doesn't exists or is not a directory".format(cmd_args[1]))
            raise SystemExit
           

        # Verify that the replica path is an existing directory  
        elif((path.exists(cmd_args[2]) == False) or (path.isdir(cmd_args[2]) == False) ):
            customlog.error("Provided replica path argument ({}) doesn't exists or is not a directory".format(cmd_args[2]))
            raise SystemExit
             

        # Check that the path to write log to is an existing directory 
        elif((path.exists(cmd_args[4]) == False) or (path.isdir(cmd_args[4]) == False) ):
            customlog.error("Provided log path argument ({}) doesn't exists or is not a directory".format(cmd_args[4]))
            raise SystemExit
            
        
        # Finally, log a success message when all verifications are passed. And return True boolean for debugging and test purpose
        else:
            customlog.info("Succesfully passed {} as source path, {} as replica path , {} as log path, synchronization interval of {} seconds.".format(cmd_args[1], cmd_args[2],cmd_args[4],cmd_args[3]))
            return True
    
    except Exception as thrown_exception:
           customlog.debug( "Some error or exception encountered while validating the command line arguments.\n {} \n {}".format(thrown_exception,traceback.format_exc()) )   



def file_handler(dcmp, log_file):

    """A function that handles file operations related to synchronization task. 

    The function takes two arguments, directory comparison object and user define path for the log file.
    Basic log file configuration is implemented on the log path provided and a suffix file name is added.
    """     

    # Log configuration for synchronization operations using the user provided log path
    user_log_file = logging.FileHandler(log_file)
    user_log_file.setLevel(logging.DEBUG)
    user_log_file.setFormatter(log_format)
    customlog.addHandler(user_log_file)
    
    
    # See the comment on line 53
    try:

        # Specific file comparison and according operations
        for name in dcmp.diff_files:
            # Source and target definition
            source = dcmp.left + "\\" + name
            target = dcmp.right + "\\" + name
            
            # Conversion to path for safety
            source_path = os.path.normpath((r'%s' % source))
            target_path = os.path.normpath((r'%s' % target))

            # Copy, overwrite and log the file operation.
            # Since the problem statement specifies one-way synchronization, the file will only be updated in the target/replica path.
            shutil.copy(source_path, target_path)
            customlog.info("{} in {} has been updated in {}".format(name, dcmp.left, dcmp.right))
            
        # forward operations   
        if dcmp.left_only:
            # A list holding the paths
            list_of_files_to_copy = dcmp.left_only

            # Loop through the list to define the source and target and perform file operations accordingly.
            for file in list_of_files_to_copy:
                # Path definitions
                source = dcmp.left + "\\" + file
                target = dcmp.right + "\\" + file
                source_path = os.path.normpath((r'%s' % source))
                target_path = os.path.normpath((r'%s' % target))

                # Conditional copy based on whether the object is a file or a directory          
                if path.isdir(source_path) == True:
                    shutil.copytree(source_path,   target_path)
                    customlog.info("Copying {} to {}".format(source_path, target_path))
                if path.isfile(source_path) == True:
                    shutil.copyfile(source_path,   target_path) 
                    customlog.info("Copying {} to {}".format(file, target_path.removesuffix("\\"+file)))

        # backward operations    
        if dcmp.right_only:
            # A list holding the paths
            list_of_files_to_remove = dcmp.right_only
            for file in list_of_files_to_remove:
                source = dcmp.right + "\\" + file
                # target = dcmp.right + "\\" + file
                source_path = os.path.normpath((r'%s' % source))
 
                # Determine if the path is directory or a file and perform operation accordingly
                if path.isdir(source_path) == True:
                    shutil.rmtree(source)       
                    customlog.info("{} has been deleted from {}".format(file, source_path.removesuffix("\\"+file)))
                if path.isfile(source_path) == True:
                    os.remove(source_path)
                    customlog.info("{} has been deleted from {}".format(file, source_path.removesuffix("\\"+file)))

        # sub directory handling via loop   
        for sub_dcmp in dcmp.subdirs.values():
            file_handler(sub_dcmp, log_file)
       
    except Exception as thrown_exception:
           customlog.debug("Some error or exception encountered.\n {}. \n {}.".format(thrown_exception, traceback.format_exc())) 