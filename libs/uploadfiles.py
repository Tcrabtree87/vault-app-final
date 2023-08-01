#
#   Author:  Jeffrey Goodwin
#   Date: 3/17/2023
#   Routines to upload files / folders to a folder on eDiscovery shared drive
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
from datetime import datetime
import time
import sys
import csv
import threading


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload


# pull API wrappers from a folder

sys.path.insert(1, '/libs')
sys.path.insert(1, '/libs/async')


# my wrappers for API's

from driveapi import *
from sheetapi import *
from vaultapi import *
from traceapi import *
from config import *
    


    
def make_folder(service, parent_id, subfolder_name) :

    #parent_list = parent.get('files',[])
    #parent_folder = parent_list.pop()
    #parent_id = parent_folder.get('id')
    #print("parent_id=",parent_id)
    
    
    
    file_metadata = {
    'parents' : [parent_id],
    'name': subfolder_name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    subfolder = service.files().create(body=file_metadata,  supportsAllDrives=True,
                                    fields='id').execute()
    print ('Folder ID: %s' % subfolder.get('id'))

    return subfolder
      
    
    
def upload_file(service, drive_id, parent_id, file):

    #Insert new file.
    #Returns : Id's of the file uploaded
    #
 
    try:
        # create drive api client


        file_metadata = {'name': file.name,  'parents' : [parent_id]}
        
        print(file_metadata)

        media = MediaFileUpload(file.name,chunksize=1024*1024,resumable=True)
        
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id', supportsAllDrives='yes').execute()
                                      
        
        #response = None
        #while response is None:
        #    status, response = file.next_chunk()
        #    print("status=", status, "response=", response)
        
        #if status:
        #    print("Uploaded %d%%." % int(status.progress() * 100))
        
        if (file == None):
            print("error empty file returned")
            return None
            
        print("file=", file)

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

    return file.get('id')
  
    

def upload_files(creds, log_dir, matter_name, matter_id):


    try:
        driveservice = build('drive', 'v3', credentials=creds)
        file_count = 0
        dir_count = 0
        log_file = ""

        drive = find_shared_drives(driveservice)
        print("drive=", drive)
        drive_id = drive['id']
        
        folder = find_folder(driveservice, drive, "'"+"city-attorney-downloads"+"'")
        
        print(folder)
        temp = folder['files']
        temp = temp[0]
        parent_id = temp['id']
        print("parent_id=", parent_id)
        
        
        # check to see if the folder exits
        # if it does, then alter the name
        # so that there is not a duplicate
        
        check_name = "name=" + "'" + matter_name + "'" + " and mimeType='application/vnd.google-apps.folder'"
    
        response = driveservice.files().list(q=check_name,
                                driveId=drive_id,
                                corpora='drive',
                                includeItemsFromAllDrives=True,
                                supportsAllDrives=True
                                ).execute()
    
    
        today = ""
    
        for item in response.get('files', []):
            print("item=", item)
            if(item['name'] == matter_name):
                # modify the name to make it
                # unique
                today = "-" + datetime.now().strftime("%Y-%m-%d, %H:%M:%S")


        
        matter_folder =  make_folder(driveservice, parent_id, matter_name+today)
        print("matter_folder=", folder)
        matter_folder_id = matter_folder['id']
        
        vault_folder = make_folder(driveservice, matter_folder_id, "vault")
        
        vault_folder_id = vault_folder['id']
        
        
        
        log_file = matter_name+"-drive-transfer-log.csv"
        handle = open(log_dir+'\\'+log_file, 'w' )
        
        # current directory
        curdir = os.getcwd()
        print("curdir=",curdir)
        
        
        # let's change back to the matter directory
        os.chdir(curdir + '\\' + matter_id)
        
        
        # get a list of the folders
    
        # get a list of the current directories
        dirs = os.scandir()
        
        # current directory
        curdir = os.getcwd()
        print("curdir=",curdir)
        
 
        for directory in dirs:
        
            print(directory)
            print(directory.name)
            print(directory.is_file())
           
            # upload vault extracts
            
            if(directory.name == "downloads"):
                
                os.chdir(curdir+'\\'+directory.name)
                subdirs = os.scandir()
                
                for subdir in subdirs:
                
                    if(subdir.is_file() == True):
                        continue
                
                    sub_folder =  make_folder(driveservice, vault_folder_id, subdir.name)
                    print(subdir, " ", sub_folder)
                    sub_folder_id = sub_folder['id']
                    dir_count += 1

                    os.chdir(curdir+'\\'+directory.name+'\\'+subdir.name)

                    files = os.scandir()
                    for file in files :
                        time.sleep(1)
                        file_id = upload_file(driveservice, drive_id, sub_folder_id, file)
                        print(file.name, " ", file_id)
                        
                        file_count +=1
                        
                        #handle = open(curdir+'\\'+directory.name+"-transfer-log.csv", 'a+' )
                        entry = '"'+subdir.name+'"'+ ',' +       \
                                '"'+file.name+'"' + ',' +   \
                                '"'+file_id+'"' + ',' +     \
                                '"'+str(datetime.now()) + '"' + '\n'
                        handle.write(entry)
                        #handle.close()
             
                print("dir_count=", dir_count, " file_count=", file_count)
                        
            if(directory.name == "work"):
                
                    os.chdir(curdir+'\\'+directory.name+ '\\' + 'mbox')
                    
                    sub_folder =  make_folder(driveservice, matter_folder_id, 'mbox')
                    print(subdir, " ", sub_folder)
                    sub_folder_id = sub_folder['id']
                    #dir_count += 1

                    files = os.scandir()
                    
                    for file in files :
                        time.sleep(1)
                        file_id = upload_file(driveservice, drive_id, sub_folder_id, file)
                        print(file.name, " ", file_id)
                        
                        file_count +=1
                        
                        #handle = open(curdir+'\\'+directory.name+"-transfer-log.csv", 'a+' )
                        entry = '"'+subdir.name+'"'+ ',' +       \
                                '"'+file.name+'"' + ',' +   \
                                '"'+file_id+'"' + ',' +     \
                                '"'+str(datetime.now()) + '"' + '\n'
                        handle.write(entry)
                        #handle.close()
        handle.close()

        return log_file
        
        
    except HttpError as err:
            time.sleep(10)
            error_string = str(err)
            #error_429 = str(err).find("429")
            #if (error_429 != -1) :
            #    exceed_quota_count +=1
            #
            #    print("bump the exceed_quota_count in main",exceed_quota_count)
            
            print("HttpError=",err,datetime.now())
               
            #write_error(get_error_fname(), error_string)
            #time.sleep(10)
            pass
    