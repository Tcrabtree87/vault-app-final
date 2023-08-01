#
#   Author:  Jeffrey Goodwin
#   Date: 03/24/2023
#
#   Get a report of the size of the exports before downloading
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
#start_count = 0

def make_count_entry(export, matter_name):

    export_name = export.get('name')
    createTime = export.get('createTime')
    export_id = export.get('id')
    query = export.get('query')
    
    stats = export.get('stats')
    

    totalArtifactCount = stats['totalArtifactCount']
    exportedArtifactCount = stats['exportedArtifactCount']
    
    sizeInBytes = stats.get('sizeInBytes',0)

        
    startTime = query['startTime']
    endTime = query['endTime']
    #terms = query['terms']
    #terms = terms.replace('"',"'")
    
    count_entry     =  '"' + matter_name + '"' + ','
    count_entry     +=  '"' + export_name + '"' + ','
    count_entry     += '"' + export_id + '"' + ','
    #count_entry     += '"' + terms + '"' + ','
    count_entry     += '"' + totalArtifactCount + '"' + ','
    count_entry     += '"' + exportedArtifactCount + '"' + ','
    count_entry     += '"' + str(sizeInBytes) + '"' + ','
    count_entry     += '"' + createTime + '"' + ','
    count_entry     += '"' + startTime + '"' + ','
    count_entry     += '"' + endTime + '"' + ','
    count_entry     += '\n'
    
    return count_entry



def download_export (export, matter_name, export_log_fname) :


    if 'cloudStorageSink' in export:
    
        rawdir = export['name']
          
        rawdir2 = rawdir.replace(">","")
        directory = rawdir2.replace(" ","")
        
        export_name = export.get('name')
        createTime = export.get('createTime')
        export_id = export.get('id')
        query = export.get('query')
        
        stats = export.get('stats')
        
        totalArtifactCount = stats.get('totalArtifactCount')
        exportedArtifactCount = stats.get('exportedArtifactCount')
        sizeInBytes = stats.get('sizeInBytes')
        
        startTime = query['startTime']
        endTime = query['endTime']

        count_entry = make_count_entry(export, matter_name)
        
        print("count_entry=", count_entry)
        
        export_log_handle = open(export_log_fname,'a+' )
        export_log_handle.write(count_entry)
        export_log_handle.close()
        
        return 



def export_report(vaultservice, config, matter_id):

    global exceed_quota_count
    
    matter = get_matter_byid(vaultservice, matter_id)
    
    matter_name = matter['name']
    
    #matter_name = config['matterName']
    
    # configure the vault API wrappers
    configure_vault_api(config, matter_name)

    # configure the api trace_fname
    configure_trace_api(config, matter_name,'log-files')

    try:
    
        export_log_fname = 'log-files' + '\\' + matter_name + config['exportsFname']
    
        export_list = [] 
        
        exports =  get_exports(vaultservice, matter_id)
        
    
        header  =   '"' + "Matter Name" + '"' + ','
        header  +=  '"' + "Export Name"  + '"' + ','
        header  +=  '"' + "Export ID"  + '"' + ','
        #header  +=  '"' + "Search Terms"  + '"' + ','
        header  +=  '"' + "totalArtifactCount"  + '"' + ','
        header  +=  '"' + "exportedArtifactCount"  + '"' + ','
        header  +=  '"' + "sizeInBytes"  + '"' + ','
        header  +=  '"' + "Create Time"  + '"' + ','
        header  +=  '"' + "startTime"  + '"' + ','
        header  +=  '"' + "endTime"  + '"' + ','
        header  +=  '"' + "filenames"  + '"' + '\n'
            
        export_log_handle = open(export_log_fname,'w' )
        export_log_handle.write(header)
        export_log_handle.close()
            
        for count, export in enumerate(exports) :

            export_name = export.get('name')
            
            print("export ", count, "-->" , export_name)
            
            download_export (export, matter_name, export_log_fname)
  
    except HttpError as err:
            time.sleep(10)
            error_string = '"'+"main exit, HttpError="+str(err)+"total_queries=",str(total_queries)+'"'
            error_429 = str(err).find("429")
            if (error_429 != -1) :
                exceed_quota_count +=1

                print("bump the exceed_quota_count in main",exceed_quota_count)
            
            print("HttpError=",err,datetime.now())
               
            write_error(get_error_fname(), error_string)
            time.sleep(10)
            pass
