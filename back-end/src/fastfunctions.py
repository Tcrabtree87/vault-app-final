
#
#   Author:  Jeffrey Goodwin
#   Date: 05/19/2023
#   These are support routines for the FASTAPI backend framework to the UI
#
#   Copyright 2023, All Rights Reserved
#
#   To Run this program, you must first setup a project in Google Cloud, 
#   with a project name and ID, API Key, and Client private Key
#
#
#
#

from __future__ import print_function

import os
import os.path
import json
import requests
import time
from datetime import datetime
import sys
import threading
import importlib.util as ilu
import shutil 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import storage
#from google.cloud import bigquery
from google.auth import compute_engine


# pull API wrappers from a folder

sys.path.insert(1, '/libs')

src_dir     = "src"
log_dir     = "log-files"
data_dir    = "./data-files/"

#numQueries
#numExports = 0
#exportCount = 0
#downloadCount = 0
downloadsDone = False
reportsDone = False
exceed_quota_count = 0

# my wrappers for API's

from driveapi   import *
from sheetapi   import *
from vaultapi   import *
from config     import *
from traceapi   import *
from utils      import *
from uploadfiles import *

# api's for this module
from vaultui import *
from sendemail import *
from exportreport import *
from sftpvault import *
# constants used in GUI
from guitypes import *
from configsettings import *


downloadStatus  = ""
mboxStatus      = ""
driveStatus     = ""
sftpStatus      = ""


def downloads_done():

    global downloadsDone

    return downloadsDone


def reports_done():

    global reportsDone

    return reportsDone
    
def download_status():

    global downloadStatus
    
    return downloadStatus

    
def mbox_status():

    global mboxStatus
    
    return mboxStatus

def drive_status():

    global driveStatus
    
    return driveStatus

def sftp_status():

    global sftpStatus
    
    return sftpStatus

#### progress update functions 

#
#### update configuration file stored by matter_id
#
def create_matter_config(matter_id, query_config):

    print("query_config=", query_config)
    
    matterConfig = json.loads(query_config)
   
    # write it out to a file
    # reformat matter_config, and store in .json file with
    # with matter_id as file name
    
    config_data = json.dumps(matterConfig,indent=2)

    matter_config_fname = data_dir + matter_id +".json"
    
    handle = open(matter_config_fname,'w+' ) # overwrites the file
    handle.write(config_data)
    handle.close()
    
    print("config_data=", config_data)
    
    with open(matter_config_fname) as f:
        data = f.read()
        
    # reconstructing the data as a dictionary
    matterConfig = json.loads(data)
            
    print("matterConfig=", matterConfig)

    return matterConfig

#
#### functions that map to FASTAPI requests
#

async def get_my_matter_by_name (creds, matter_name):
    
    vaultservice = build('vault', 'v1', credentials=creds)
    
    matter = get_vault_matter(vaultservice, matter_name)
    
    return matter




async def create_my_matter (creds, config, matter_name):
    
    vaultservice = build('vault', 'v1', credentials=creds)
    adminservice = build('admin', 'directory_v1', credentials=creds)

    
    try:
        print("config=", config)
    
        matter = create_vault_matter(vaultservice, matter_name, "")
        
        print("matter=", matter)
        
        matter_id = matter['matterId']
        powerUser = config['powerUser']
        print("powerUser=", powerUser)
        
        
        
        # share the matter with Tyler

        #permission = add_matter_permission(vaultservice, matter_id, powerUser)
        #TODO change to poweruser
        # comment out below because I am setting it update
        # into Tyler's account itself now....
        #user = get_user(adminservice,'tyler.crabtree@lacity.org')
        
        #account_id = user.get('id')
        
        #print("account_id=", account_id)
        
        #permission = add_collaborator(vaultservice, matter_id, account_id)
        
        
        #print("permission=", permission)

        
    except HttpError as err:
        error_string = "err=" + str(err) + str(datetime.now())
        print(error_string)
        print("HttpError=",HttpError)
        matter = {}    
    
    print("in create_matter : ", matter);
    
    return matter



def create_my_org_queries (creds, config):
    
    vaultservice = build('vault', 'v1', credentials=creds)
    
    print("in create_my_queries")
    
    print("config=", config);
    matter_id = config['matterId']
    matter_config_fname = data_dir + matter_id +".json"
    
    num_queries = create_vaultui_org_queries(vaultservice, config, log_dir)

    print("in create_my_queries : ", num_queries);
    
    update_progress_config(matter_id, matter_config_fname);
    
    return num_queries
    


def create_my_queries (creds, config):
    
    vaultservice = build('vault', 'v1', credentials=creds)
    
    print("in create_my_queries")
    
    print("config=", config);
    matter_id = config['matterId']
    matter_config_fname = data_dir + matter_id +".json"
    
    num_queries = create_vaultui_queries(vaultservice, config, log_dir)

    print("in create_my_queries : ", num_queries);
    
    update_progress_config(matter_id, matter_config_fname);
    
    return num_queries
    
#
#### support routines from download_my_exports()    
#

def make_count_entry(export, matter_name):

    export_name = export.get('name')
    createTime = export.get('createTime')
    export_id = export.get('id')
    query = export.get('query')
    stats = export.get('stats')
    
    totalArtifactCount = stats['totalArtifactCount']
    exportedArtifactCount = stats['exportedArtifactCount']
    sizeInBytes = stats['sizeInBytes']
    startTime = query['startTime']
    endTime = query['endTime']
    terms = query['terms']
    #terms = terms.replace('"',"'")
    
    count_entry     =  '"' + matter_name + '"' + ','
    count_entry     +=  '"' + export_name + '"' + ','
    count_entry     += '"' + export_id + '"' + ','
    count_entry     += '"' +  terms + '"' + ','
    count_entry     += '"' + totalArtifactCount + '"' + ','
    count_entry     += '"' + exportedArtifactCount + '"' + ','
    count_entry     += '"' + sizeInBytes + '"' + ','
    count_entry     += '"' + createTime + '"' + ','
    count_entry     += '"' + startTime + '"' + ','
    count_entry     += '"' + endTime + '"' + ','


        
    filenames = ""
    
    for sinkFile in export['cloudStorageSink']['files']:
    
        filenames   += sinkFile['objectName'].split('/')[-1] + ';' \
                    + "size=" + sinkFile['size'] + ';' \
                    + "md5hash=" + sinkFile['md5Hash'] + ';'
    
    count_entry     += '"' + filenames + '"' + '\n'
    
    return count_entry

    
def download_export (gcpClient, export, matter_name, export_log_fname) :

    numDownloads = 0
    
    print("export=", export)
    
    matter_id = export['matterId']
    
    downloadDirectory = matter_id + "\\" + "downloads" 
    
    if not os.path.exists(downloadDirectory):
            os.makedirs(downloadDirectory)
            
    if not os.path.exists(matter_id + "\\" + "work" + "\\" + "downloads"):
            os.makedirs(matter_id + "\\" + "work" + "\\" + "downloads")
            
    if not os.path.exists(matter_id + "\\" + "mbox" ):
            os.makedirs(matter_id + "\\" + "mbox" )
            

    if 'cloudStorageSink' in export:
    
        rawdir = export['name']
          
        rawdir2 = rawdir.replace(">","")
        directory = downloadDirectory + "\\" + rawdir2.replace(" ","")
        
        export_name = export.get('name')
        createTime = export.get('createTime')
        export_id = export.get('id')
        query = export.get('query')
        stats = export.get('stats')
        
        totalArtifactCount = stats['totalArtifactCount']
        exportedArtifactCount = stats['exportedArtifactCount']
        sizeInBytes = stats['sizeInBytes']
        startTime = query['startTime']
        endTime = query['endTime']

        count_entry = make_count_entry(export, matter_name)
        print("export=", export)
        print("count_entry=", count_entry)
        
        export_log_handle = open(export_log_fname,'a+' )
        export_log_handle.write(count_entry)
        export_log_handle.close()
           
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        #open the hash file so we can make it
        md5_hashfile = open(directory+'\\'+export['id']+".md5",'a')
        
        for sinkFile in export['cloudStorageSink']['files']:
            
            real_fname = sinkFile['objectName'].split('/')[-1]
            
            filename = '%s/%s' % (directory, sinkFile['objectName'].split('/')[-1])
            objectURI = 'gs://%s/%s' % (sinkFile['bucketName'],
                                        sinkFile['objectName'])
                                        
            print("filename=", filename)
                                            
            #print('get %s to %s' % (objectURI, filename))
                
            bucket = gcpClient.bucket(sinkFile['bucketName'])
                    
            blob = bucket.blob('source_blob_name');
            handle = open(filename, 'wb+')
            print("handle=", handle)
             
            time.sleep(5)
            #time.sleep(int(sleep_time) * (exceed_quota_count+1) )
            
            ### temp comment out real download
            result = gcpClient.download_blob_to_file(objectURI, handle)
            
            
            
            if(result != None):
                # unexpected result, log it
                error_fname = matter_name + "-error.csv"
                write_error(error_fname, "error from gcpClient.download_blob_to_file="+str(result))

            numDownloads += 1
            
            md5_hashfile.write(sinkFile['md5Hash']+" "+real_fname+"\n")
            
            print("result=", result)
            
        md5_hashfile.close() 

        numDownloads += 1
        
        return numDownloads
#
#### this routine maps to the FASTApi call
#
def download_my_exports (creds, config, parms):

    global exceed_quota_count


    global downloadsDone
    #global numExports
    #global exportCount
    #global downloadCount
    
    global downloadStatus
    global mboxStatus    
    global driveStatus   
    global sftpStatus    
    
    exceed_quota_count = 0
    start_count = 0
    downloadsDone = False
    numExports = 0
    downloadCount = 0
    exportCount = 0
    
    print("parms=", parms)
    
    matter_id   = parms['matterId']
    recipient   = parms['recipient']
    #exportType  = parms['exportType']
    #queueSize   = parms['queueSize']
    options = parms['options']
    seperateMBOX = options['seperateMBOX']
    uploadToDrive = options['uploadToDrive']
    uploadToSFTP = options['uploadToSFTP']
    
    
    try:
    
        vaultservice = build('vault', 'v1', credentials=creds)
    
        # gcloud auth application-default login
        gcpClient = storage.Client()
        
        matter = get_matter_byid(vaultservice, matter_id)
        
        matter_name = matter['name']
        
        # configure the vault API wrappers
        configure_vault_api(config, matter_name)
        
        # configure the api trace_fname
        configure_trace_api(config, matter_name, log_dir)
        
        export_log_fname = matter_name + config['exportsFname']
       
       # Call the Vault API
        matter = get_vault_matter(vaultservice, matter_name)
        #matter = get_matter(vaultservice, matter_name)
        print("matter=",matter)
        matter_id = matter.get('matterId')
        print("matter_id=",matter_id)
        
        start_count = config['startCount']
        
        #testing_code(vaultservice, matter_id)
        
        export_list = [] 
        
        exports =  get_exports(vaultservice, matter_id)
        
        
        
        numExports = len(exports)
        
        set_num_exports(numExports)
        
        # check to see if the number of exports is zero.  It could be that 
        # they were never created, or that they were manually deleted or the amount
        # of time (15 days) that vault keeps them has expired.
        
        if (numExports == 0) :
        
            downloadsDone = noDownloads
            
            return
            
        
        
        print("numExports=", numExports)
        
        if(start_count == 1):
        
            header  =   '"' + "Matter Name" + '"' + ','
            header  +=  '"' + "Export Name"  + '"' + ','
            header  +=  '"' + "Export ID"  + '"' + ','
            header  +=  '"' + "Search Terms"  + '"' + ','
            header  +=  '"' + "totalArtifactCount"  + '"' + ','
            header  +=  '"' + "exportedArtifactCount"  + '"' + ','
            header  +=  '"' + "sizeInBytes"  + '"' + ','
            header  +=  '"' + "Create Time"  + '"' + ','
            header  +=  '"' + "startTime"  + '"' + ','
            header  +=  '"' + "endTime"  + '"' + ','
            header  +=  '"' + "filenames"  + '"' + '\n'
                
            export_log_handle = open(log_dir + '\\'+ export_log_fname,'w' )
            export_log_handle.write(header)
            export_log_handle.close()
            
        # make a directory where the downloadsDone
        # are going to go
        # matter_id/downloads
        
        #### download defined states
        #downloadingFromVault    = 1
        #seperatingMBOX          = 2
        #uploadingToDrive        = 3
        #uploadingToFTP          = 4 
        #downloadsFinished       = 5
        #downloadsNotAvailable   = 6
        
        
        notProcessed = '<font color="black"> Not Processed'
        processing   = '<font color="red"> Processing'
        finishedProcessing = '<font color="blue"> Finished Processing'
        
        downloadStatus  = notProcessed
        mboxStatus      = notProcessed
        driveStatus     = notProcessed
        sftpStatus      = notProcessed
        
        
         
        #
        ##### Download from Vault
        #
        
        downloadsDone = downloadingFromVault
        
        downloadStatus = processing
        
        
        # let the progress indicator in the GUI initialize
        time.sleep(10) 
            
        for count, export in enumerate(exports) :
        
            export_name = export.get('name')
            
            print("export ", count, "-->" , export_name)
            
            exportCount += 1
            
            set_export_count(exportCount)
            
            # for now, start from the beginning each time
            #if(count+1 < start_count):
            #    continue
                
            
            # TEMP: TODO uncomment this to do the real download
            numDownloads = download_export (gcpClient, export, matter_name, log_dir + '\\' + export_log_fname)
            #numDownloads = 5 ## temp, remove later
            print("numDownloads=", numDownloads)
            
            
            downloadCount += numDownloads
            
            print("downloadCount=", downloadCount)
            
            set_download_count(downloadCount)
            
        
        # go into the matter directory
        
        # current directory
        curdir = os.getcwd()
        print("curdir=",curdir)
        
        #os.chdir(curdir) #+'\\'+matter_id)
                
        message = gmail_send_message(creds, matter_name + " Vault Download Log", export_log_fname, recipient )
        
        print("message=", message)

        downloadStatus = finishedProcessing
        
        #
        ##### Separating MBOX
        #



        if(seperateMBOX == True):
        
            downloadsDone = seperatingMBOX
            
            mboxStatus = processing
        
            ### now make a copy of the exports into a 'work' directory
        
            time.sleep(5)
            # path 
            path = curdir+'\\'+ matter_id
                
            # Source path 
            src = curdir + '\\' + matter_id + '\\' + 'downloads'
            
                
            # Destination path 
            dest = curdir + '\\' + matter_id + '\\' + 'work' + '\\' + 'downloads'
            
            # if the destination directory exists, we should just remove it.
            # we're going to unzip it anyway
            
            print("remove directory")
            
            if os.path.exists(dest):
                shutil.rmtree(dest)
                
            
                
            # Copy the content of 
            # source to destination 
            try: 
                destination = shutil.copytree(src, dest, dirs_exist_ok=True) 
            except OSError as err:
                print("err=", err)
                #shutil.copytree(src, dest)
                pass 
            
            print("destination=", destination)
            # print(destination) prints the
            # path of newly created file
            
            ### change to the work directory, and unzip it
            
            
            os.chdir(curdir + '\\' + matter_id + '\\' + 'work')
            process_tree()
            
            # Destination path 
            mboxdir = curdir + '\\' + matter_id + '\\' + 'work' + '\\' + 'mbox'
            
            if not os.path.exists(mboxdir):
                # make the directory
                os.makedirs(mboxdir)
                
            # now selectively copy only the .mbox files 
            
            print("copy the .mbox files over")
            
            # Copy the content of
            # source to destination
            for root, dirs, files in os.walk(dest):
                print("root=", root, "dirs=", dirs, "files=", files)
                
                for file in files:
                    if file[-5:].lower() == '.mbox':
                        print("file=", file)
                        print("ext=", file[-5:].lower())
                        shutil.copy(os.path.join(root, file), os.path.join(mboxdir, file))
            
            time.sleep(5)
            
            mboxStatus = finishedProcessing
        
     
        
        # let's change back to the main directory
        os.chdir(curdir )

        if(uploadToDrive == True):
        
            #
            ##### Uploading to Drive
            #
            
            downloadsDone = uploadingToDrive
            
            driveStatus = processing
            
            time.sleep(5)
            
            
            drive_log_file = upload_files(creds, log_dir, matter_name, matter_id)
            
            # let's change back to the main directory
            os.chdir(curdir + '\\' )
            
            
            message = gmail_send_message(creds, matter_name + " Drive Transfer Log", drive_log_file, recipient )
            
            print("message=", message)
            
            driveStatus = finishedProcessing


        #
        ##### Uploading to SFTP
        #
        if (uploadToSFTP == True):
        
            downloadsDone = uploadingToSFTP
            
            sftpStatus = processing
        
            sftpPassword = config['sftpPassword']
            sftpUsername = config['sftpUsername']
            sftpIP = config['sftpIP']
            
            sftp_url = "sftp://" + sftpUsername + "@" + sftpIP
            
            print("sftp_url=", sftp_url)
            
            key_file = sftpUsername
            
            ## temp TODO: put this in general settings
            #sftp_url = "sftp://ext_jeffrey_goodwin@34.170.234.24"
            #key_file = "ext_jeffrey_goodwin-nopass"
            print("sftp_url=", sftp_url)
            print("key_file=", key_file)
            sftp_log_file = vault_tosftp(matter_id, matter_name, log_dir, sftp_url, sftpPassword, key_file)
            
            
            time.sleep(15)
            
            # let's change back to the main directory
            os.chdir(curdir + '\\' )
            
            #### last thing is to email the reportsDone
            
            message = gmail_send_message(creds, matter_name + " SFTP Transfer Log", sftp_log_file, recipient )
            
            print("message=", message)
            
            sftpStatus = finishedProcessing
            
        # update configuration file
        
        matter_config = get_matter_config (matter_id, data_dir)
    
        matter_config ['matterState'] = matter_state_downloaded
        matter_config ['downloadCount'] = get_download_count()
    
        config_data = update_matter_config (matter_id, data_dir, matter_config)    
        
        # mark downloads complete
            
        downloadsDone = downloadsFinished
            
        
        print("downloadsDone=", downloadsDone)
        
        #print("exports=", exports)
        
    except HttpError as err:
            time.sleep(10)
            error_string = '"'+"main exit, HttpError="+str(err)+"total_exports=",str(len(exports))+'"'
            error_429 = str(err).find("429")
            if (error_429 != -1) :
                exceed_quota_count +=1

                print("bump the exceed_quota_count in main",exceed_quota_count)
            
            print("HttpError=",err,datetime.now())
               
            write_error(get_error_fname(), error_string)
            time.sleep(10)
            pass
    

def export_my_matter (creds, config, parms):

    global reportsDone
    
    start_count = 0
    reportsDone = 0

    print("parms=", parms)
    
    matter_id   = parms['matterId']
    recipient   = parms['recipient']
    exportType  = parms['exportType']
    queueSize   = parms['queueSize']

    vaultservice = build('vault', 'v1', credentials=creds)
    
    matter = get_matter_byid(vaultservice, matter_id)
    
    matter_name = matter['name']

    # configure the vault API wrappers
    configure_vault_api(config, matter_name)

    # configure the api trace_fname
    configure_trace_api(config, matter_name, log_dir)
    
    exports = run_exports(vaultservice, matter_id, exportType, int(queueSize))
    
    print("len of exports=", len(exports))  
    
    # update the number of exports in the configuration file
    
    # update the configuration file with the changed 
    # matter state
    
    matter_config = get_matter_config (matter_id, data_dir)
    
    matter_config ['matterState'] = matter_state_exported
    matter_config ['exportCount'] = len(exports)
    
    config_data = update_matter_config (matter_id, data_dir, matter_config)
    
    
    # make report for exports, and email it out
    
    export_report(vaultservice, config, matter_id)
    
    filename = matter_name + "-exports.csv"
    
    message = gmail_send_message(creds, "Vault Export Report", filename, recipient )
        
    print("message=", message)

    reportsDone = True

    return 

    
def count_my_matter (config, creds, matter_id, recipient):

    start_count = 0
    
    #set_grand_total()
    #set_total_queries()
    vaultservice = build('vault', 'v1', credentials=creds)
    
    matter = get_matter_byid(vaultservice, matter_id)
    
    matter_name = matter['name']
    
    print("config=", config)

    # configure the vault API wrappers
    configure_vault_api(config, matter_name)

    # configure the api trace_fname
    configure_trace_api(config, matter_name, log_dir)
    
    grand_total = count_saved_queries(vaultservice, matter, start_count)
    
    filename = matter_name + "-counts.csv"
    #print("recipient=", recipient)
    #recipient = "jeffrey.goodwin@lacity.org"
    
    # update the configuration file with the changed 
    # matter state
    
    matter_config = get_matter_config (matter_id, data_dir)
    
    matter_config ['matterState'] = matter_state_counted
    
    config_data = update_matter_config (matter_id, data_dir, matter_config)
    
    # send email message with count report

    message = gmail_send_message(creds, "Vault Count Report", filename, recipient )
        
    print("message=", message)

    return grand_total

    

#
####  test functions
#
def my_thread (config, creds, event):

    print(config)
    print(creds)
    
    
    # see if we can access the matter
    matter_id = config['matterId']
    matter_name = config['matterName']

    # configure the vault API wrappers
    configure_vault_api(config, matter_name)

    # configure the api trace_fname
    configure_trace_api(config, matter_name, log_dir)

    # create API services
    
    adminservice = build('admin', 'directory_v1', credentials=creds)
    driveservice = build('drive', 'v3', credentials=creds)
    sheetservice = build('sheets', 'v4', credentials=creds)
    vaultservice = build('vault', 'v1', credentials=creds)
    
    # create service object for spreadsheets
    sheets = sheetservice.spreadsheets()
    
    matter = get_matter_byid(vaultservice, matter_id)
    
    print(matter)

    time.sleep(30)
    event.set()
    
 
    return

async def await_my_thread (config, creds):

    # see if we can access the matter
    matter_id = config['matterId']
    matter_name = config['matterName']

    # configure the vault API wrappers
    configure_vault_api(config, matter_name)

    # configure the api trace_fname
    configure_trace_api(config, matter_name, log_dir)
    
    
    # create API services
    
    adminservice = build('admin', 'directory_v1', credentials=creds)
    driveservice = build('drive', 'v3', credentials=creds)
    sheetservice = build('sheets', 'v4', credentials=creds)
    vaultservice = build('vault', 'v1', credentials=creds)
    
    # create service object for spreadsheets
    sheets = sheetservice.spreadsheets()
    
    matter = get_matter_byid(vaultservice, matter_id)
    
    time.sleep(30)
    
    print(matter)

    return matter

####  test functions

