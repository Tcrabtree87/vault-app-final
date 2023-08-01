#
#   Author:  Jeffrey Goodwin
#   Date: 04/01/2023
#   This routine, is the backend for the UI.  It processes requests for
#   each action panel to call Google Vault API's, do reporting, and send out
#   out reports. 
#
#   Copyright 2023, All Rights Reserved
#
#   To Run this program, you must first setup a project in Google Cloud, 
#   with a project name and ID, API Key, and Client private Key
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

from typing import Union
from fastapi import FastAPI, Response, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
#from pydantic import BaseModel

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from google.cloud import storage
#from google.cloud import bigquery
from google.auth import compute_engine


# pull API wrappers from a folder

sys.path.insert(1, '/libs')

src_dir     = "src"
log_dir     = "log-files"
data_dir    = "./data-files/"

reports_done = False

# my wrappers for API's

from driveapi   import *
from sheetapi   import *
from vaultapi   import *
from config     import *
from traceapi   import *

# api's for this module
from vaultui import *
from sendemail import*
from exportreport import*
from fastfunctions import*



# ingest the config file
config = ingest_config("config.json")


if(config == None):
    print("error, configuration file not found")
    exit()
    
creds = authenticate()

count_threads = [] 

#temp, TODO: remove
#exportProgress = 0
downloadProgress = 0
#numQueries = 0       

origins = [
    "http://localhost",
    "http://localhost:1180",
]



try:

    # instantiate fastapi.  note: main is hypercorn application
    app = FastAPI()


    # enable CORS.  allow from/to anywhere for now

    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    
    @app.get("/create_downloads")
    async def create_downloads(export_parms: str):
        #global downloadProgress
    
        #downloadProgress = 0
        
        
        vaultservice = build('vault', 'v1', credentials=creds)

        # send email
        parms = json.loads(export_parms)
        print("parms=", parms)
        matter_id = parms['matterId']
        recipient = parms['recipient']
        options = parms['options']
        
        #queries = get_queries ( vaultservice, matter_id )
        
        #numQueries = len(queries)
        
        #set_num_queries(numQueries)
      
        #event = threading.Event()
        t = threading.Thread(name='counts thread', target=download_my_exports, args=(creds, config, parms))
        #count_threads += [[t, event]]
        t.start()
        
        return {"matter" : "send email response"}
    
    
    @app.get("/create_exports")
    async def create_exports(export_parms: str):
    
        global count_threads         
        #global numQueries
        #global exportProgress
        
        # num queries
        exportProgress = 0
        
        vaultservice = build('vault', 'v1', credentials=creds)

        # get parms
        parms = json.loads(export_parms)
        print("parms=", parms)
        matter_id = parms['matterId']
        recipient = parms['recipient']
        
        queries = get_queries ( vaultservice, matter_id )
        
        #numQueries = len(queries)
        
        #set_num_queries(numQueries)
      
        #event = threading.Event()
        t = threading.Thread(name='counts thread', target=export_my_matter, args=(creds, config, parms))
        #count_threads += [[t, event]]
        t.start()
 
        return {"matter" : "send email response"}


    @app.get("/create_org_queries")
    async def create_org_queries(query_config: str):
    
        # ok, we need to update the configuration file with all 
        # of any potentially changed entries like the date range,
        # queries, or custodians.  However, the matter state and creation 
        # status should be preserved from the exiting configuration file
        # stored on disk
        myConfig = json.loads(query_config)
        matter_id = myConfig['matterId']
        
        #matter_config_fname = matter_id +".json"
        matter_config_fname = data_dir + matter_id +".json"
        
        with open(matter_config_fname) as f:
            data = f.read()
            
        # reconstructing the data as a dictionary
        matter_config = json.loads(data)
        print("matter_config=", matter_config)
        
        matterState = matter_config['matterState']
        completionStatus = matter_config['completionStatus']

        matterConfig = create_matter_config(matter_id, query_config)
        
        # need to save it back out to disk
        
        ##############################################
        matterConfig = json.loads(query_config)

        matterConfig['matterState']     = matterState
        matterConfig['completionStatus']  = completionStatus
    
        # write it out to a file
        # reformat matter_config, and store in .json file with
        # with matter_id as file name
    
        config_data = json.dumps(matterConfig,indent=2);
        matter_config_fname = data_dir + matter_id +".json"
        #matter_config_fname = matter_id +".json"
        handle = open(matter_config_fname,'w+' ) # overwrites the file
        handle.write(config_data)
        handle.close()
        
        ##############################################
        vaultservice = build('vault', 'v1', credentials=creds)
        queries = get_queries ( vaultservice, matter_id )
        
        numQueries = len(queries)
        
        if(numQueries > 0):
            matterConfig['numQueries'] = numQueries
            matterConfig['searchCount']= numQueries
            return {"matter" : matterConfig}
        
        t = threading.Thread(name='create_my_org_queries', target=create_my_org_queries, args=(creds, matterConfig))
        t.start()
        
        
        print("matterConfig=", matterConfig)
        
        return {"matter" : matterConfig}


    @app.get("/create_queries")
    async def create_queries(query_config: str):
    
        # TODO:  need to merge this logic into update routines.
        # ok, we need to update the configuration file with all 
        # of any potentially changed entries like the date range,
        # queries, or custodians.  
        
        # However, the matter state and creation 
        # status should be checked for logical progression to a new state 
        # from the exiting configuration file
        # stored on disk
        
        myConfig = json.loads(query_config)
        matter_id = myConfig['matterId']
        
        #matter_config_fname = matter_id +".json"
        matter_config_fname = data_dir + matter_id +".json"
        
        with open(matter_config_fname) as f:
            data = f.read()
            
        # reconstructing the data as a dictionary
        matter_config = json.loads(data)
        print("matter_config=", matter_config)
        
        matterState = matter_config['matterState']
        
        completionStatus = matter_config['completionStatus']

        matterConfig = create_matter_config(matter_id, query_config)
        
        # need to save it back out to disk
        
        ##############################################
        matterConfig = json.loads(query_config)

        matterConfig['matterState']     = matterState
        matterConfig['completionStatus']  = completionStatus
    
        # write it out to a file
        # reformat matter_config, and store in .json file with
        # with matter_id as file name
    
        config_data = json.dumps(matterConfig,indent=2);
        matter_config_fname = data_dir + matter_id +".json"
        #matter_config_fname = matter_id +".json"
        handle = open(matter_config_fname,'w+' ) # overwrites the file
        handle.write(config_data)
        handle.close()
        
        ##############################################
        vaultservice = build('vault', 'v1', credentials=creds)
        queries = get_queries ( vaultservice, matter_id )
        
        numQueries = len(queries)
        
        if(numQueries > 0):
            matterConfig['numQueries'] = numQueries
            matterConfig['searchCount']= numQueries
            return {"matter" : matterConfig}
        
        t = threading.Thread(name='create_my_queries', target=create_my_queries, args=(creds, matterConfig))
        t.start()
        
        
        print("matterConfig=", matterConfig)
        
        return {"matter" : matterConfig}


    @app.get("/get_query_progress")
    def get_query_progress():
    
        progress = vault_query_progress()
        
        print("progress=", progress)
        
        numQueries = progress['numQueries']
        searchCount = progress ['searchCount']
        creationStatus = progress['creationStatus']
        
        return {"numQueries" : numQueries, "searchCount" : searchCount, "creationStatus" : creationStatus }
        
    @app.get("/get_count_progress")
    def get_count_progress():
        grandTotal = get_grand_total ()
        numQueries = get_num_queries()
        
        queryCount =  get_query_count()
        
        return {"queryCount" : queryCount, "grandTotal" : grandTotal, "numQueries" : numQueries}

    @app.get("/get_downloads_progress")
    
    def get_downloads_progress():
    
		
        downloadsDone = downloads_done()
        numExports = get_num_exports()
        exportCount = get_export_count()
        downloadCount = get_download_count()
    
    
        downloadStatus  = download_status()
        mboxStatus      = mbox_status()
        driveStatus     = drive_status()
        sftpStatus      = sftp_status()
    
        exportStatus = {"numExports" : numExports,          \
                        "exportCount" : exportCount,        \
                        "downloadCount" : downloadCount,    \
                        "downloadsDone" : downloadsDone,    \
                        "downloadStatus" : downloadStatus,  \
                        "mboxStatus" : mboxStatus,          \
                        "driveStatus" : driveStatus,        \
                        "sftpStatus" : sftpStatus,
                        }
    
        return exportStatus

    @app.get("/get_export_progress")
    def get_export_progress():

        reportsDone = reports_done();
        queryCount = get_query_count()
        numQueries = get_num_queries()
        numExports = get_num_exports()
        exportCount = get_export_count()
        
        return {"numQueries" : numQueries, "queryCount" : queryCount, "numExports" : numExports,  "exportCount" : exportCount, "reportsDone" : reportsDone}

    @app.get("/create_matter")
    async def create_matter(matter_config: str):
        
        myconfig = json.loads(matter_config)
        matter_name = myconfig['matterName']

        matter = await create_my_matter(creds, config, matter_name)
        matter_id = matter['matterId']

        matterConfig = create_matter_config(matter_id, matter_config)
        matterConfig['matterId'] = matter_id
        matterConfig['matterState'] = matter['state']
        
        # write it out to a file
        # reformat matter_config, and store in .json file with
        # with matter_id as file name
        #data = json.loads(matterConfig)
        config_data = json.dumps(matterConfig,indent=2)
  
        ## TODO: consolidate this file update into an update routine.
  
        matter_config_fname = data_dir + matter_id + ".json"
  
        handle = open(matter_config_fname,'w+' ) # overwrites the file
        handle.write(config_data)
        handle.close()
    
        return {"matter" : matterConfig}
   
    
    @app.get("/get_matter_by_name")
    async def get_matter_by_name(matter_name: str):
    
        print("get_matter_by_name", matter_name)
        vaultservice = build('vault', 'v1', credentials=creds)

    
        matter = await get_my_matter_by_name(creds,matter_name)
        
        print("matter=", matter)
        
        matter_id = matter['matterId']
        
        #matter_config_fname = matter_id +".json"
        matter_config_fname = data_dir + matter_id +".json"

        with open(matter_config_fname) as f:
            data = f.read()
            
        # reconstructing the data as a dictionary
        matter_config = json.loads(data)
        
            
        print("matter_config=", matter_config)
        #print("matter=", matter)
        
        queries = get_queries ( vaultservice, matter_id )
        currentNumQueries = len(queries)
        exports = get_exports(vaultservice, matter_id)
        currentNumExports = len(exports)
        
        print("currentNumQueries=", currentNumQueries)
        print("currentNumExports=", currentNumExports)
        
        #numQueries = len(queries)
        
        return {"matter" : matter_config}
        #return {"matter" : "test"}
        
       
    
    @app.get("/count_matter")
    async def count_matter(export_parms: str):
    
        global count_threads 
        grand_total = 0
        
        parms = json.loads(export_parms)
        print("parms=", parms)
        matter_id = parms['matterId']
        recipient = parms['recipient']

        event = threading.Event()
        t = threading.Thread(name='counts thread', target=count_my_matter, args=(config, creds, matter_id,recipient))
        count_threads += [[t, event]]
        t.start()
 

        return {"grand_total" : grand_total}


    @app.get("/update_settings")
    async def update_settings(parms : str):
    
        global config
    
        settings = json.loads(parms)
        
        print("settings=", settings)

        ## TODO: implement actual save of new settings in update_my_settings
        config = await update_my_settings(config, creds, settings)
        
        #config = new_config
        #print("config=",config)
            
        return {"settings": settings}


    @app.get("/get_settings")
    
    async def get_settings():
    
        # return system configuration file.   This functions
        # get's called when the general system dialog on the GUI
        # is opened
            
        return {"settings": config}
        
        
        
    @app.get("/get_orginfo")
    async def get_orginfo():
    
        
        orginfo_fname = 'system-files\\orginfo.csv'

        with open(orginfo_fname) as f:
            data = f.read()
            
        
        return {"orgInfo" : data}

####  test functions ####        

    @app.get("/")
    async def read_root():
        global count_threads    
        status = ""    
        for thread in count_threads:
            t = thread[0]
            event = thread[1]
            status += "thread=" + str(t) + "--" + str(event.is_set())
            
        return {"Thread": "State- " + status}
    
    @app.get("/await_thread")
    
    async def await_thread():
        
        matter = await await_my_thread(config, creds)
        return {"matter": "matter- " + str(matter) }
        
    @app.get("/start_thread")
    async def start_thread():
    
        global count_threads    

        event = threading.Event()
        t = threading.Thread(name='counts thread', target=my_thread, args=(config, creds, event,))
        count_threads += [[t, event]]
        t.start()

        return {"Thread": "State- "+str(event.is_set())}
####  test functions ####        

except:
        pass
