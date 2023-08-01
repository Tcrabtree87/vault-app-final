#
#   Author:  Jeffrey Goodwin
#   Date: 02/05/2023
#   Routine to unzip .mbox files in a tree created by Google Vault routines
#   that download exports
#   
#   Copyright 2023, All Rights Reserved
#
#   To Run this program, you must first setup a project in Google Cloud, 
#   with a project name and ID, API Key, and Client private Key
#
#

from __future__ import print_function

import os.path
import json
import requests
import datetime 
import time
import sys

#from datetime import datetime
import zipfile
# utility to copy files
import shutil

#from google.cloud import storage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# pull API wrappers from a folder

sys.path.insert(1, '/libs')

# my wrappers for API's

from driveapi import *
from sheetapi import *
from vaultapi import *
from traceapi import *
from config import *
    
exceed_quota_count = 0

def unzip(filename):

    with zipfile.ZipFile(filename, mode="r") as archive:
        archive.extractall("")

    with zipfile.ZipFile(filename, mode="r") as archive:
        for info in archive.infolist():
            fname = info.filename
            print(f"Filename: {info.filename}")
            #print(f"Modified: {datetime.datetime(*info.date_time)}")
            print(f"Modified: {datetime(*info.date_time)}")
            print(f"Normal size: {info.file_size} bytes")
            print(f"Compressed size: {info.compress_size} bytes")
            print("-" * 20)
            with zipfile.ZipFile(fname, mode="r") as archive:
                archive.extractall("")
            
    



def process_tree():


    # get a list of the current directories
    dirs = os.scandir()
    print ("dirs=", dirs)

    # current directory
    curdir = os.getcwd()
    print("curdir=",curdir)
    
    # now go into the target dirctory
    for count, direntry in enumerate(dirs) :
        if(direntry.is_file() == False) :
            print("num=", count, " ", direntry.name)
            print("type=", direntry.is_file())
            
            # navigate into the downloads directory
            
            if(direntry.name == "downloads"):
                os.chdir(curdir+'\\'+direntry.name)

    # get a list of the current directories
    dirs = os.scandir()
    print ("dirs=", dirs)

    # current directory
    curdir = os.getcwd()
    print("curdir=",curdir)
    
    for count, direntry in enumerate(dirs) :
        #print(direntry)
        print("num=", count, " ", direntry.name)
        print("type=", direntry.is_file())
        
        if(direntry.is_file() == False) :
            os.chdir(curdir+'\\'+direntry.name)
            print("curdir=",os.getcwd())
            # now locate the .zip file
            targetdir = os.scandir()
            for target in targetdir :
                #print(target.name)
                name = target.name
                
                if(name.find(".zip") != -1) :
                    print("name=", name)
                    #print(".zip file ?", name.find(".zip"))
                    
                    # this is the .zip file
                    # unzip it
                    
                    # this is how you unzip it --> 
                    unzip(name)
                    
                    base_name = name[:4]
                    mbox_name = base_name + '.mbox'
                    # now make a copy of it in 
                    # the .mbox directory
                    # add in next run TODO:
                    #shutil.copy2(mbox_name, curdir+'\\'+'mbox'+mbox_name) # complete target filename given
                    
                
            
        
    
    #os.chdir()
    
    return
    
