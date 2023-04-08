# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import traceback
import multiprocessing.connection
import psutil

import data
import functions
import components.communicator


PID_FILE = functions.unixify_join(
    data.settings_directory,
    "pid_list.txt"
)

def is_pid_running(pid):
    try:
        if not psutil.pid_exists(pid):
            return False
        
        process = psutil.Process(pid)
        if not process.is_running():
            return False
        
        name = process.name().lower()
        if "python" in name or "exco":
            return True
        
        return False
    except Exception:
#        traceback.print_exc()
        return False

def check_opened_excos():
    try:
        if os.path.isfile(PID_FILE):
            with open(PID_FILE, "r+", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            with open(PID_FILE, "w+", encoding="utf-8") as f:
                lines = []
            
        filtered_list = [ str(os.getpid()) ]
        
        for l in lines:
            pid = l.strip()
            if not pid.isdigit():
                continue
            
            pid = int(pid)
            if is_pid_running(pid):
                filtered_list.append(str(pid))
        
        with open(PID_FILE, "w+", encoding="utf-8") as f:
            f.write('\n'.join(filtered_list))
        
        return len(filtered_list)
    except:
        return -1

def send_raw_command(command):
    connection = multiprocessing.connection.Client(
        (components.communicator.ADDRESS, components.communicator.PORT),
        authkey=components.communicator.PASSWORD.encode('utf-8')
    )
    connection.send((
        "PRE-START {}".format(os.getpid()),
        command
    ))
    connection.close()
        