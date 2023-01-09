import os
import logging
import pytest

from utilityfunctions import cmd_argument_validator 
from utilityfunctions import file_handler


@pytest.fixture(autouse=True)
def setup_and_teardown():
    try:
        # Setups: 
        # Create directories for use across multiple test cases

        # Create test source directory
        test_source_dir = os.mkdir("testsourcedir")
        # Create test replica directory
        test_replicad_ir = os.mkdir("testreplicadir")
        # Create test log directory
        test_log_dir = os.mkdir("testlogdir")
        
        # Holder for tests cases
        yield

        # Teardown: clean ups after test cases
        #  Remove the created directories after test case has been run

        # Remove test source directory
        os.rmdir("testsourcedir")
        # Remove test replica directory
        os.rmdir("testreplicadir")
        # Remove test log directory
        os.rmdir("testlogdir")
    
    except OSError as error :
        logging.error(error)


def test_incomplete_argument():
    with pytest.raises(SystemExit):
        cmd_argument = []
        cmd_argument_validator(cmd_argument)

def test_invalid_interval_argumentTwo():
    source =r"testsourcedir"
    replica =r"testreplicadir"
    log=r"testlogdir"
    interval = "five seconds"
    cmd_args = [source, replica, interval, log]
    with pytest.raises(SystemExit):
        cmd_argument_validator(cmd_args)
      


          

