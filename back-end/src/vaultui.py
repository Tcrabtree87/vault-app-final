
#
#   Author:  Jeffrey Goodwin
#   Date: 05/07/2023
#
#   Routine to make final queries by timeslot, across all accounts, with correspondence to 
#   specific domains / custodians.  This version is adapated from the script based one to 
#   work with the GUI.
#
#   Copyright 2023, All Rights Reserved
#
#   To Run this program, you must first setup a project in Google Cloud, 
#   with a project name and ID, API Key, and Client private Key
#
# pull API wrappers from a folder

import sys
import time
import json


sys.path.insert(1, '/libs')
src_dir     = "src"
log_dir     = "log-files"
data_dir    = "./data-files/"



# my wrappers for API's

from vaultapi   import *
from config     import *
from traceapi   import *

# the number of queries that are created
search_count = 0
# total searches to be created
num_queries = 0
# query creation Status
query_creation_status = ""

  
def vault_query_progress():
    global search_count
    global num_queries
    global query_creation_status

    progress = {"numQueries" : num_queries, "searchCount" : search_count, "creationStatus" : query_creation_status}

    return progress
    
    

def update_progress_config(matter_id, matter_config_fname):

    
    progress = vault_query_progress()
    
    ###  update config file ###
    
    #matter_config_fname = data_dir + matter_id +".json"

    with open(matter_config_fname) as f:
        data = f.read()
        
    # reconstructing the data as a dictionary
    matter_config = json.loads(data)
        
    print("matter_config=", matter_config)
    
    matter_config['numQueries'] = progress['numQueries']
    matter_config['searchCount'] = progress['searchCount']
    matter_config['completionStatus'] = progress['creationStatus']
    temp = ""
    print("type of temp", type(temp))
    
    temp = json.dumps(matter_config, indent=2)
    print("type of temp\n", type(temp))
    print("temp=", temp)
    
    handle = open(matter_config_fname,'w+' ) # overwrites the file
    handle.write(temp)
    handle.close()
        


    
def convert_json_list(itemList, myType):

    new_list = []
    
    for i, item in enumerate(itemList) :
    
        temp = json.dumps(item)
        temp = temp.replace('\\r','')
        temp1 = json.loads(temp)
        entry = temp1[myType]
        new_list += [entry]
        
    return new_list
  
def create_vaultui_queries(vaultservice, config, log_dir):
  
  
  
    global num_queries
    global search_count
    global query_creation_status

    search_count = 0  
    query_creation_status = ""
 
 
    matter_id = config['matterId']
    matter_name = config['matterName']
 

    configure_vault_api(config, matter_name)
    configure_trace_api(config, matter_name, log_dir)
    
    
    try:
    

        
        matter = get_matter_byid(vaultservice, matter_id)
     
        # these are the time slots
        timeslot = config['timeSlot']

        custodians= config['custodianEmails']
        #custodians_config = config['custodianEmails']
        #custodians = convert_json_list(custodians_config, "custodian")
        terms_config = config['terms']
        terms = convert_json_list(terms_config, "term")
        num_custodians = len(custodians)
        num_terms = len(terms)
        

        # the number of queries below should
        # equal the number actually created in 
        # Google Vault
        num_queries = num_custodians * num_terms
        
        config['numQueries'] = num_queries

        startTime = timeslot['startTime']
        endTime = timeslot['endTime']
        
        byCustodianOnly = config['byCustodianOnly']
        
        
        for custodian in custodians :
        
            #custodian_name = custodian[0]
            #custodian_email = custodian[1]
            custodian_email     = custodian['custodian']
            custodian_type      = custodian['type']
            print("custodian_type=", custodian_type)

            
            print("custodian=", custodian);
            custodian_email = custodian_email.replace('"','')
            print("custodian_email=", custodian_email);
        
            for count, search in enumerate(terms) :
            
                # let's see it
                print("------------------------")
                print("search=",search)
                print("------------------------")
            
                search = search.replace('""','"')
                print("search=",search)
            

                final_search = search
                
                if(byCustodianOnly == "True"):
                    query_name = custodian_email
                else:
                    query_name = custodian_email +"--"+final_search
                
                query_name = query_name.replace("*","_")
                query_name = query_name.replace(":","_")
                #query_name = query_name.replace("@lacity.org","")
                query_name = query_name.replace('"',"")

                #saved_query =  map_queryrow_parms(query_name, "ACCOUNT", custodian, final_search, timeslot)
                saved_query =  map_queryrow_parms(query_name, "ACCOUNT", custodian_email, custodian_type, final_search, timeslot)
                
                time.sleep(2)
                print("saved_query=", saved_query)

                result = create_saved_query(vaultservice, matter_id, saved_query)
                
                print("result=", result)

                
                if(result != None):
                    search_count += 1
                else:
                    query_creation_status = "Errors creating Queries<br> <br>"
                    
           
        if (num_queries != search_count):
            query_creation_status = 'Errors creating Queries'
        else:
            query_creation_status = 'Queries Created'
            
        config['searchCount'] = search_count
            
        return config     
        
    except HttpError as err:
            error_string = "err=" + str(err) + str(datetime.now())
            query_creation_status = "Error: <br> <br>" + str(err)
            print("query_creation_status=", query_creation_status)
            print(error_string)
            print("HttpError=",HttpError)
            #try to log the API parameters too
            api_parms = {}
            api_parms ["creds"] = creds
            api_parms ["vaultservice"] = vaultservice
            api_parms ["driveservice"] = driveservice
            api_parms ["sheetservice"] = sheetservice

  
            write_log(get_error_fname(),matter_name,error_string+str(api_parms))

            pass

  
def create_vaultui_org_queries(vaultservice, config, log_dir):
  
  
  
    global num_queries
    global search_count
    global query_creation_status

    search_count = 0  
    query_creation_status = ""
 
 
    matter_id = config['matterId']
    matter_name = config['matterName']
 

    configure_vault_api(config, matter_name)
    configure_trace_api(config, matter_name, log_dir)
    
    
    try:
    

        
        matter = get_matter_byid(vaultservice, matter_id)
     
        # these are the time slots
        timeslot = config['timeSlot']

        #custodians_config = config['custodianEmails']
        #custodians = convert_json_list(custodians_config, "custodian")
        
        organizations = config['organizations']
        
        #print("organizations_config=", organizations_config)
        
        #organizations = convert_json_list(organizations_config, "organization")
        
        print("organizations=", organizations)
        
        terms_config = config['terms']
        terms = convert_json_list(terms_config, "term")
        
        #num_custodians = len(custodians)
        num_organizations = len(organizations)
        
        num_terms = len(terms)
        

        # the number of queries below should
        # equal the number actually created in 
        # Google Vault
        #num_queries = num_custodians * num_terms
        num_queries = num_organizations * num_terms
        
        config['numQueries'] = num_queries

        startTime = timeslot['startTime']
        endTime = timeslot['endTime']
        
        byOrganizationOnly = config['byOrganizationOnly']
        
        
        #for custodian in custodians :
        for organization in organizations :
        
            print("organization=", organization)
            #continue
        
            #custodian_name = custodian[0]
            #custodian_email = custodian[1]
            
            #print("custodian=", custodian);
            #custodian = custodian.replace('"','')
            #print("custodian=", custodian);
            
            organization_name = organization['organization']
            org_id = organization['organization_id']
            print("organization_name=", organization_name)
            print("org_id=", org_id)
            
            for count, search in enumerate(terms) :
            
                # let's see it
                print("------------------------")
                print("search=",search)
                print("------------------------")
            
                search = search.replace('""','"')
                print("search=",search)
            

                final_search = search
                
                #if(byCustodianOnly == "True"):
                #    query_name = custodian
                #else:
                #    query_name = custodian +"--"+final_search
                

                
                if(byOrganizationOnly == "True"):
                    query_name = organization_name
                else:
                    query_name = organization_name +"--"+final_search
                
                
                query_name = query_name.replace("*","_")
                query_name = query_name.replace(":","_")
                #query_name = query_name.replace("@lacity.org","")
                query_name = query_name.replace('"',"")

                #saved_query =  map_queryrow_parms(query_name, "ACCOUNT", custodian, final_search, timeslot)
                
                saved_query = map_saved_query_orgunit(query_name, final_search, org_id, timeslot)
                
                time.sleep(2)
                print("saved_query=", saved_query)

                result = create_saved_query(vaultservice, matter_id, saved_query)
                
                print("result=", result)
                
                if(result != None):
                    search_count += 1
                else:
                    query_creation_status = "Errors creating Queries<br> <br>"

        if (num_queries != search_count):
            query_creation_status = 'Errors creating Queries'
        else:
            query_creation_status = 'Queries Created'
            
        config['searchCount'] = search_count
            
        return config     
        
    except HttpError as err:
            error_string = "err=" + str(err) + str(datetime.now())
            query_creation_status = "Error: <br> <br>" + str(err)
            print("query_creation_status=", query_creation_status)
            print(error_string)
            print("HttpError=",HttpError)
            #try to log the API parameters too
            api_parms = {}
            api_parms ["creds"] = creds
            api_parms ["vaultservice"] = vaultservice
            api_parms ["driveservice"] = driveservice
            api_parms ["sheetservice"] = sheetservice

  
            write_log(get_error_fname(),matter_name,error_string+str(api_parms))

            pass
