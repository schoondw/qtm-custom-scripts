"""
Batch process for modifying selected range in a batch process

Uses the REST interface to control QTM.

QTM must be running and loaded with the project that is being processed.
    * The option for closing the measurement when a new one is loaded must be turned on (don't open new
      windows)
    * The QTM python script in which the custom menu/command is defined must be loaded (QTM script: modify_range_script.py).

Loops through the data folders in the project    

QTM data folder structure:
    * Subject
        * Session (containing QTM files)
    
For each QTM data file:
    * Tell QTM to load the file
        * Loop until QTM acknowledges the file has been loaded
    * Send a QTM script command to QTM
    * Script command in QTM 
        * modifies the selected range according to script parameters (QTM script: modify_range_script.py)
    * Save the file
    
"""

#import sys
import argparse
import os
import requests
import time
#import xml.etree.ElementTree as ET

# Some Global variables
IP_CONNECTION = "127.0.0.1"
REST_IP_PREFIX = f"http://{IP_CONNECTION}:7979/api/scripting/qtm/"
REST_IP_PREFIX_EXP = f"http://{IP_CONNECTION}:7979/api/experimental/command_v2/"
REST_IP_PREFIX_EXP_OLD = f"http://{IP_CONNECTION}:7979/api/experimental/command/"
PROJECT_FOLDER = "C:\\Users\\est\\QTM_local\\Qualisys"
DATA_FOLDER = os.path.join(PROJECT_FOLDER,"Data")

# Setting to false means not to send load commands to QTM,
#LOAD_QTM_FILES = True
SAVE_QTM_FILES = True

def batch_run_main():
    """ 
    Main processing function 
    """

    rest_cmd = f"{REST_IP_PREFIX}gui/send_command"
    rest_load_file= f"{REST_IP_PREFIX_EXP}load_file"
    rest_ack_job= f"{REST_IP_PREFIX_EXP}ack_job"
    rest_save_file = f"{REST_IP_PREFIX_EXP_OLD}save_file"
    rest_run_command = ["mod_range"]

    print(f"EXPLORING: <{DATA_FOLDER}>")

    subjects = os.listdir(path=DATA_FOLDER)
    print(f"Sessions: {subjects}")
    for subject in subjects:
        full_capture_name = os.path.join(DATA_FOLDER,subject)
        if os.path.isdir(full_capture_name):
            sessions = os.listdir(path=full_capture_name)
            for session in sessions:
                full_session_name = os.path.join(full_capture_name, session)
                if os.path.isdir(full_session_name):
                    files = os.listdir(path=full_session_name)
                            
                for file in files:
                    # print(f"    File: {file}")
                    if file.endswith('.qtm'):
                        print(f"    File: {file}")
                        fullname = os.path.join(full_session_name,file)
                        print(f"Loading {fullname}")
                        resp = requests.post(rest_load_file,json={'file_name':fullname})
                        print(f"Load File response: {resp.content}")
                        r = resp.json()['id']
                        # print(f"r is <{r}>")
                        key_finished = resp.json()['finished']
                        while not key_finished:
                            print(f"Z-", end='')
                            time.sleep(1)
                            # resp = requests.post(rest_ack_job,json={'job_id':str(r)}) # QTM 2023.2 and earlier
                            resp = requests.post(rest_ack_job,json={'id':str(r)}) # From QTM 2023.3
                            # print(f"Ack Response: <{resp.content}>")
                            key_finished = resp.json()['finished']
                        print()
                        print(f"Done loading {fullname}")

                        # Run an internal QTM Script to parse information
                        requests.post(rest_cmd,json=rest_run_command)
                        time.sleep(2) # Fixed time out: make sure it is long enough to execute the command!
                        print(f"Sent QTM command {rest_run_command}")

                        # file_count += 1
                        if SAVE_QTM_FILES:
                            print(f"Saving {fullname}")
                            resp = requests.post(rest_save_file,json={"FileName":fullname})
                            print(f"Save File response: {resp.content}")
                            time.sleep(3) # Fixed time out: make sure it is long enough to save the files!
                        else:
                            print(f"File not saved")
                        print()


def batch_run_parse_arguments():
    """
    Parse the command line and set global variables for processing.
    """
    global PROJECT_FOLDER
    global DATA_FOLDER
    #global LOAD_QTM_FILES
    global SAVE_QTM_FILES

    parser = argparse.ArgumentParser(
        prog="batch_run_main", 
        description="Apply a script to all data in a QTM project"
        )
    parser.add_argument("projectfolder",type=str,help="Project folder to pull from",default=PROJECT_FOLDER)
    #parser.add_argument('-n',"--noload",help="Don't Load files",action='store_true')
    parser.add_argument('-n',"--nosave",help="Don't Save files",action='store_true')

    args = parser.parse_args()

    PROJECT_FOLDER = args.projectfolder
    DATA_FOLDER = os.path.join(PROJECT_FOLDER,"Data")
    #LOAD_QTM_FILES = not args.noload
    SAVE_QTM_FILES = not args.nosave

    print(f"Project Folder: {PROJECT_FOLDER}")
    #print(f"Load: {LOAD_QTM_FILES}")
    print(f"Save: {SAVE_QTM_FILES}")


def main():
    batch_run_parse_arguments()
    batch_run_main()

if __name__ == "__main__":
    main()
