import time
import json

from datetime import datetime

from googleapiclient.errors import HttpError

from traceapi import *



# get the count total for a saved query    

# trace support
   
# we need to identify these as reprocessed    
counts_fname = ""       #"-totals.csv"
error_fname = ""        #"-error.csv"
severe_error_fname = "" #"-severe-errs.csv"
trace_fname = ""        #"-api.csv"
warning_fname = ""      #"-warning.csv" 

# count variables
query_count = 0
grand_total = 0
num_queries = 0

# export variables
num_exports = 0
export_count = 0

download_count = 0

exceed_quota_count = 0


# set progress variables

def set_num_exports(numExports):

    global num_exports

    num_exports = numExports
    
    
def set_num_queries(numQueries):

    global num_queries

    num_queries = numQueries



def set_query_count(queryCount):

    global query_count

    query_count = queryCount
    
    
    
def set_export_count(exportCount):

    global export_count

    export_count = exportCount
    
    
def set_download_count(downloadCount):

    global download_count

    download_count = downloadCount
    

### get progress variables

def get_download_count():

    global download_count
    
    return download_count


    
def get_export_count():

    global export_count

    return export_count

def get_grand_total():

    global grand_total

    return grand_total
    
def get_query_count():

    global query_count
    
    return query_count
    
    
def get_num_exports():

    global num_exports

    return num_exports
    
def get_num_queries() :
    global num_queries

    return num_queries


##
#   configure vault API with config file parameters
##
def configure_vault_api(config, matter_name) :

    global counts_fname
    global error_fname
    global severe_error_fname
    global trace_fname
    global warning_fname
    
    counts_fname = matter_name + config['countsFname']
    error_fname = matter_name + config['errorFname']        
    severe_error_fname = matter_name + config['severeFname'] 
    warning_fname = matter_name + config['warningFname']  
    trace_fname = matter_name + config['apiFname']


def get_error_fname():
    global error_fname

    return error_fname

##
# Google Vault Operations
##
    # *****************
    # work with matters
    # *****************
    
def get_vault_matter(service, name) :
    token = "1"
    while (token != None):
        if(token == "1"):
            token = ""
        
        results = service.matters().list(state='OPEN', pageSize=100, pageToken=token).execute()
        #print("in get_matter, results = ", results)
        token = results.get('nextPageToken')
        #print("pageToken=", token)
        matters = results.get('matters', [])
        
        for matter in matters:
            #print(matter)
            if(matter.get('name') == name):
                return matter
                
    return None

def get_matter_byid(service, matter_id) :
   
    # Call the Vault API
    matter = service.matters().get(matterId=matter_id).execute()
                
    return matter


def create_vault_matter(service, matter_name, matter_description):

    matter_content = {
      'name': matter_name,
      'description': matter_description,
    }
    
    matter = service.matters().create(body=matter_content).execute()
    
    return matter


def delete_matter(service, matter_id) :

    time.sleep(.1)
    
    # trash the matter
    wanted_matter = {
        'name': 'trash',
        'description': 'trash'
    }
    
    updated_matter = service.matters().update(
        matterId=matter_id, body=wanted_matter).execute()
        
    time.sleep(.1)
    
    # first you have to close the matter
    close_response = service.matters().close(matterId=matter_id, body={}).execute()
    
    #print("close_response=", close_response)
    
    time.sleep(.1) 
    
    # now we can delete it
    service.matters().delete(matterId=matter_id).execute()
    
    time.sleep(.1)
    
    matter = get_matter_byid(service, matter_id)
    
    return matter # should be 'None'
    
    # *****************
    # count queries
    # *****************
 
def check_operation_errors(operation, query):
    
    if(operation == None):
        # error, could not create the operation for this query
        # log the error and continue
        error_string = "cannot create operation, None returned" 
        write_log(error_fname,query, error_string )
        return -1
    
    error_code = operation.get('error')
                
    if (error_code != None) :
        # error, could not create the operation for this query
        # log the error and continue
        error_string = "cannot create operation, code=" + str(error_code) + str(operation)
        write_log(error_fname,query, error_string )
        return -2
    
    response = operation.get('response')
                
    if (response == None) :
        # error, could not create the operation for this query
        # log the error and continue
        error_string = "empty response" + str(operation)
        write_log(error_fname,query, error_string )
        return -3
    
    mailCountResult = response.get('mailCountResult')
    
    if (mailCountResult == None) :
        # error, could not create the operation for this query
        # log the error and continue
        error_string = "empty mailCountResult" + str(operation)
        write_log(error_fname,query, error_string )
        return -4

    # NOTE: We do not check the account errors here on purpose.  
    #       The reason is, we want to enter to the retry loop
    #       where this routine is called from, to retry the 
    #       operation reads up to five times, and give Google Vault
    #       more time to overcome temporary synchronization issues
    
    #accountErrors = mailCountResult.get('accountCountErrors')                       

    #if (accountErrors == None) :
    #    # error, could not create the operation for this query
    #    # log the error and continue
    #    error_string = "accountErrors" + str(operation)
    #    write_log(error_fname,query, error_string )
    #    return -5

 
    return None
 
 
def count_saved_queries(service, matter, query_startcount):
    global counts_fname
    global query_count
    global warning_fname
    global error_fname
    global severe_error_fname
    global exceed_quota_count
    global grand_total
    global num_queries
    
    grand_total = 0
    total_queries = 0

    matter_id = matter['matterId']
    matter_name = matter['name']

    token = "1"
    counts_handle = open("log-files" + "\\" + counts_fname,'w+' )
    token_count = 0
    
    while(token):

        if(token=="1"):
            token=""
            
        results = service.matters().savedQueries().list(matterId=matter_id,pageSize=10000, pageToken=token).execute()
        
        token = results.get('nextPageToken')
        print ("token=", token)
        token_count += 1
        print("token_count", token_count)                     
        queries = results.get('savedQueries',[])
        
        num_queries = len(queries)
    
        for query_count, query in enumerate(queries):
        
            set_query_count(query_count + 1)

            # if retrying from a particular starting point
            # bump up the counter and continue 
            if( total_queries+1 < query_startcount):
                total_queries += 1
                continue
            
            total_queries += 1
            print("total queries=", total_queries)   

            #if(total_queries == 149):
            #    print("problem query")
            #    continue
            
            try:
                total_count = 0
                retries = 0
                accountErrors = {}
                mailCountResult = {}
                
                query_name = query.get('displayName')
                
                # there are several different types of errors that can occur
                # 1 - empty response from an operation creation or read request
                # 2 - an error code from an operation creation or read request
                # 3 - There is an empty mailCountResult
                # 4 - There are accountCountErrorsAccount in a valid mailCountResult from an operation read
                # 5 - The alloted time for polling an operation is exceeded
                # 6 - The number of retries for polling an operation is exceeded
                # 7 - An unstable network issue causes a time out deep in the client
                #     libraries.  Currently, there is no recovery from this and the program
                #     terminates
                #
                #
                operation  = count_saved_query(service, matter, query)
                
                code = check_operation_errors(operation, query)

                if(code != None):
                    continue
                
                # we should have a valid response at this point
                response = operation.get('response')

                # the mailCountResult has also been validated
                mailCountResult = response.get('mailCountResult')
                                
                accountErrors = mailCountResult.get('accountCountErrors')
                
                total_count = response.get('totalCount')

                
                while((accountErrors != None) and (retries <5)) :
                                        
                    print("account errors =", query_name,"retries=",str(retries))
                    error_string = '"'+"err=" + str(response) + " retries=" + str(retries) +'"'+','+'"'+ str(query) + '"'
                    
                    #log the warning 
                    write_log(warning_fname,query,error_string)
                    
                    # bump up the retries and sleep a little
                    retries +=1
                    time.sleep(2*retries*(exceed_quota_count+1))

                    # try again
                    
                    if(retries < 5):
                        operation = count_saved_query(service, matter, query)
                        
                        code = check_operation_errors(operation, query)

                        if(code != None):
                            retries = 5
                            continue
                            
                        # we should have a valid response at this point
                        response = operation.get('response')

                        # the mailCountResult has also been validated
                        mailCountResult = response.get('mailCountResult')
                                
                        accountErrors = mailCountResult.get('accountCountErrors')                       
                
                        total_count = response.get('totalCount')
                        
                        
            except HttpError as err:
                error_string = '"'+"counts_saved_query:HttpError=" + str(err) + '"' + ',' + '"' + str(response) + '"'
                print(error_string)
                error_429 = str(err).find("429")
                if (error_429 != -1) :
                    exceed_quota_count +=1
                    print("bump the exceed_quota_ccount in count_saved_queries",exceed_quota_count)

                time.sleep(10)
                #log the error so we can make a correction later
                write_log(severe_error_fname,query,error_string)               
                pass
            
            print("final total_count=",total_count)
            
            if(total_count == None):
                total_count = 0
            
            if(accountErrors == None):
                counts_handle.write('"'+query_name+'"'+','+'"'+str(total_count)+'"'+','+'"'+'"'+str(query)+'"'+','+'"'+str(response)+'"'+'\n')
            
                grand_total += int(total_count)
            else:
                # log the account errors
                # send it to the error file as well
                # to make it easier to find and fix
                write_log(error_fname,query, response)

        
    counts_handle.close()   
    
    return grand_total

    
def count_saved_query(service, matter, querybody):

    #global 
    global warning_fname
    global error_fname
    global exceed_quota_count
    
    matter_id = matter.get('matterId')
    matter_name = matter.get('name')
    
    # locals
    error_string = ""
    

    #todo add parameter for query options
    mail_query_options = {'excludeDrafts': True}

    # get the query name from the query wrapper
    query_name = querybody.get('displayName')

    # pull the query from inside the wrapper
    query = querybody.get('query')

    # pull the paramaters from the query needed to form the 
    # query creation
    
    
    corpus = query.get('corpus')
    dataScope = query.get('dataScope')
    searchMethod = query.get('searchMethod')
    accountInfo = query.get('accountInfo')
    terms = query.get('terms')
    startTime = query.get('startTime')
    endTime = query.get('endTime')
    mailOptions = query.get('mailOptions')
    method = query.get('method')
    
    orgUnitInfo = query.get( 'orgUnitInfo')

    # build the query
    
    mail_query = {
        'corpus': corpus,
        'dataScope': dataScope,
        'searchMethod': searchMethod,
        'accountInfo': accountInfo,
        'orgUnitInfo' : orgUnitInfo,
        'terms': terms,
        'startTime' : startTime,
        'endTime' : endTime,
        'mailOptions':mailOptions,
        'method':method
        }
    
        
    request = {
        'view': "TOTAL_COUNT",
        'query': mail_query
        }
    
    operation = operation_request(service, matter, request, querybody)

    
    if(operation == None):
        print("error, empty operation returned")
        return None


    total_count = operation.get('count')
    operation_name = operation.get('name')
    
    
    done = operation.get('done')
    totaltime = 0
    
    # if the count operation needs more time, let it run for up to sixty seconds
    
    while (operation.get('done') == None):
        sleep_time = .1 * (exceed_quota_count+1)
        time.sleep(sleep_time)

        totaltime += sleep_time
        operation = operation_read(service, matter, operation, querybody)
        
        if(operation == None):
            error_string = '"'+"encountered empty operation in count_saved_query"+'"'
            write_log(error_fname, querybody,error_string)
            
            
        if(totaltime > 60) :
            error_string='"'+"totaltime="+str(totaltime)+'"'+','+'"'+"operation="+str(operation)+'"'
            print(error_string)
            write_log(error_fname, querybody, error_string)
            
            
            time.sleep(2*sleep_time)
            break
    
    response = operation.get('response')
    
    if( response == None):  
        error_string = '"'+"encountered empty response in count_saved_query"+'"'
        write_log(error_fname, querybody, error_string)
        

    return operation
  
def reprocess_saved_query(service, matter, query):


    #global 
    global warning_fname
    global error_fname
    global counts_fname
    global exceed_quota_count
    global total_queries 
    
    
    #print("matter=", matter)
    matter_id = matter.get('matterId')
    matter_name = matter.get('name')
    total_count = 0
  
    try:
    
    
        total_count = 0
        retries = 0
        accountErrors = {}
        mailCountResult = {}
                
        query_name = query.get('displayName')
        
        # there are several different types of errors that can occur
        # 1 - empty response from an operation creation or read request
        # 2 - an error code from an operation creation or read request
        # 3 - There is an empty mailCountResult
        # 4 - There are accountCountErrorsAccount in a valid mailCountResult from an operation read
        # 5 - The alloted time for polling an operation is exceeded 
        # 6 - The number of retries for polling an operation is exceeded
        # 7 - An unstable network issue causes a time out deep in the client
        #     libraries.  Currently, there is no recovery from this and the program
        #     terminates
        #
        #
        operation  = count_saved_query(service, matter, query)
        
        code = check_operation_errors(operation, query)

        if(code != None):
            return code
        
        # we should have a valid response at this point
        response = operation.get('response')

        # the mailCountResult has also been validated
        mailCountResult = response.get('mailCountResult')
                        
        accountErrors = mailCountResult.get('accountCountErrors')
        
        total_count = response.get('totalCount')

        
        while((accountErrors != None) and (retries <5)) :
                                
            print("account errors =", query_name,"retries=",str(retries))
            error_string = '"'+"err=" + str(response) + " retries=" + str(retries) +'"'+','+'"'+ str(query) + '"'
            
            #log the warning 
            write_log(warning_fname,query,error_string)
            
            # bump up the retries and sleep a little
            retries +=1
            time.sleep(2*retries*(exceed_quota_count+1))

            # try again
            
            if(retries < 5):
                operation = count_saved_query(service, matter, query)
                
                code = check_operation_errors(operation, query)

                if(code != None):
                    retries = 5
                    total_count = code
                    continue
                    
                # we should have a valid response at this point
                response = operation.get('response')

                # the mailCountResult has also been validated
                mailCountResult = response.get('mailCountResult')
                        
                accountErrors = mailCountResult.get('accountCountErrors')                       
        
                total_count = response.get('totalCount')
            else:
                total_count = -5

    except HttpError as err:
            error_string = '"'+"counts_saved_query:HttpError=" + str(err) + '"' + ',' + '"' + str(response) + '"'
            print(error_string)
            error_429 = str(err).find("429")
            if (error_429 != -1) :
                exceed_quota_count +=1
                print("bump the exceed_quota_ccount in count_saved_queries",exceed_quota_count)


                
            time.sleep(10)
            #log the error so we can make a correction later
            write_log(error_fname,query,error_string)               
            pass
            
    print("final total_count=",total_count)          
            
    return total_count

    # ***************************
    # retrieve and create queries
    # ***************************
    
def get_query(vaultservice, matter_id, query_id):
 
    try:
        query = vaultservice.matters().savedQueries().get(matterId=matter_id, savedQueryId=query_id).execute()
		
        if (query != None):
            return query

    except HttpError as err:
            print(err)
            pass
			
    return None
 

    # create queries
 
def map_saved_query_orgunit(query_name, final_search, org_id, timeslot):


    mail_query_options = {'excludeDrafts': True}
    
    start_time = timeslot['startTime']
    end_time = timeslot['endTime']
    
    mail_query = {
        'corpus': 'MAIL',
        'dataScope': 'ALL_DATA',
        'searchMethod': 'ORG_UNIT',
        "timeZone": "America/Los_Angeles",
        "startTime": start_time,
        "endTime": end_time,
        "orgUnitInfo": {
            "orgUnitId": org_id
        },
        'terms': final_search,
        'mailOptions': mail_query_options,
    }
    saved_query = {
        'displayName': query_name,
        'query': mail_query,
    }
   
    return saved_query

   
def map_queryrow_year(matter_name, query_body, year):

    query_name = query_body.get('displayName')
    new_query_name  =  matter_name + "--" + str(query_name) + "--" + str(year['startTime'] + "-" + str(year['endTime']))
    new_query_name = new_query_name.replace(":","_")
    
    query = query_body['query']
    
    # pull the data to make the new query from the existing one
    
    corpus = query.get('corpus')
    dataScope = query.get('dataScope')
    searchMethod = query.get('searchMethod')
    timeZone = query.get('timeZone')
    # pull the start and end times from config list
    startTime = year['startTime']
    endTime = year['endTime']
    
    orgUnitInfo = query.get('orgUnitInfo')
    
    if (orgUnitInfo != None):
        orgUnitId = orgUnitInfo['orgUnitId']
        
    accountInfo = query.get('accountInfo')

    if (accountInfo != None):
        emails = accountInfo['emails']
        
    terms = query.get('terms')
    mailOptions = query.get('mailOptions')
    
    # let's take a look at what we've got so far
    #
    if ( orgUnitInfo != None):
        print("orgUnitId=", orgUnitId)
        mail_query = {
            'corpus': corpus,
            'dataScope': dataScope,
            'searchMethod': searchMethod,
            "timeZone": timeZone,
            "startTime": startTime,
            "endTime": endTime, 
            'orgUnitInfo': {
                'orgUnitId': orgUnitId,  # fix, this must be an email address
            },
            'terms': terms,
            'mailOptions': mailOptions,
        }

    if (accountInfo != None):
        print("emails=", emails)
        mail_query = {
            'corpus': corpus,
            'dataScope': dataScope,
            'searchMethod': searchMethod,
            "timeZone": timeZone,
            "startTime": startTime,
            "endTime": endTime, 
            'accountInfo': {
                'emails': emails,  # fix, this must be an email address
            },
            'terms': terms,
            'mailOptions': mailOptions,
        }

    saved_query = {
        'displayName': new_query_name,
        'query': mail_query,
    }
    
    return saved_query

 
    
def map_queryrow(custodian_name, custodian_emails, terms):

    
    mail_query_options = {'excludeDrafts': True}
    
    corpus          = "MAIL"
    dataScope       = "ALL_DATA"
    searchMethod    = "ACCOUNT"
    timeZone        = "America/Los_Angeles"
    startTime       = "2008-02-01T00:00:00Z"
    endTime         = "2019-08-31T00:00:00Z"
    terms           = terms
    #orgunit         = query_row[6]
    accounts        = custodian_emails
    
    
    
    
    
    mail_query = {
        'corpus': "MAIL",
        'dataScope': "ALL_DATA",
        'searchMethod': "ACCOUNT",
        "timeZone": "America/Los_Angeles",
        "startTime": "2008-02-01T00:00:00Z",
        "endTime": "2019-08-31T00:00:00Z",
        'accountInfo': {
            'emails': custodian_emails,  # fix, this must be an email address
        },
        'terms': terms,
        'mailOptions': mail_query_options,
    }
    saved_query = {
        'displayName': custodian_name,
        'query': mail_query,
    }
    
    return saved_query


def map_queryrow_all_accounts(query_name, terms, timeslot):
    
    mail_query_options = {'excludeDrafts': True}

    corpus          = "MAIL"
    dataScope       = "ALL_DATA"
    searchMethod    = "ACCOUNT"
    timeZone        = "America/Los_Angeles"
    
    
    mail_query = {
        'corpus': "MAIL",
        'dataScope': "ALL_DATA",
        'searchMethod': "ENTIRE_ORG",
        "timeZone": "America/Los_Angeles",
        "startTime": timeslot['startTime'],
        "endTime": timeslot['endTime'],
        #'accountInfo': {
        #    'emails': custodian,
        #},
        'terms': terms,
        'mailOptions': mail_query_options,
    }
    saved_query = {
        'displayName': query_name,
        'query': mail_query,
    }
    
    return saved_query

  
def map_queryrow_parms(query_name, search_method, custodian, custodian_type, terms, year):

    
    mail_query_options = {'excludeDrafts': True}
    
    #corpus          = "MAIL"
    dataScope       = "ALL_DATA"
    #searchMethod    = "ACCOUNT"
    timeZone        = "America/Los_Angeles"

    
    if(search_method == "ENTIRE_ORG"):
    
        mail_query = {
            'corpus': 'MAIL',  
            'dataScope': "ALL_DATA",
            'searchMethod': search_method,
            #'searchMethod': "ACCOUNT",
            "timeZone": "America/Los_Angeles",
            "startTime": year['startTime'],
            "endTime": year['endTime'],
            'terms': terms,
            'mailOptions': mail_query_options,
        }
    else:
    
        mail_query = {
            'corpus': custodian_type, # 'MAIL' OR 'GROUPS'
            'dataScope': "ALL_DATA",
            'searchMethod': search_method,
            #'searchMethod': "ACCOUNT",
            "timeZone": "America/Los_Angeles",
            "startTime": year['startTime'],
            "endTime": year['endTime'],
            'accountInfo': {
                'emails': custodian,
            },
            'terms': terms,
            'mailOptions': mail_query_options,
        }
    
    saved_query = {
        'displayName': query_name,
        'query': mail_query,
    }
    
    if ((custodian_type != 'MAIL') and (custodian_type != 'GROUPS') ):
        # this is an error
        print("error, invalid custodian type", custodian_type)
        write_log(error_fname,saved_query,"bad custodian type, should be MAIL or GROUPS")  
    
    return saved_query


def create_saved_query_orgunit(service, matter, search_name, clean_search, orgid):

    
    mail_query_options = {'excludeDrafts': True}
    matter_id = matter.get('matterId')
    
    
    mail_query = {
        'corpus': 'MAIL',
        'dataScope': 'ALL_DATA',
        'searchMethod': 'ORG_UNIT',
        "timeZone": "America/Los_Angeles",
        "startTime":"2008-02-01T00:00:00Z",
        "endTime":"2019-08-31T00:00:00Z",
        "orgUnitInfo": {
            "orgUnitId": orgid
        },
        'terms': clean_search,
        'mailOptions': mail_query_options,
    }
    saved_query = {
        'displayName': search_name,
        'query': mail_query,
    }

    response = create_saved_query(service, matter_id, saved_query)
    
    saved_query = response.get('query')
    
    return response


        
def create_saved_query(service, matter_id, saved_query):

    try:
        # log the input paramaters
        
        api_parms_string = '"'+"create_saved_query:"+str(service)+'"'+','+'"'+str(matter_id)+'"'+','+'"'+str(saved_query)+'"'

        write_log(trace_fname,saved_query,api_parms_string)


        response = service.matters().savedQueries().create(
        matterId=matter_id, body=saved_query).execute()
        
        # log the response
        
        api_response_string = '"'+"create_saved_query:"+str(response)+'"'
        
        print("response=", response)
        write_log(trace_fname,saved_query,api_response_string)
        
        return response
        
    
    except HttpError as err:
        error_string = '"'+"err="+str(err)+'"'
        print("http errror", error_string)
        
        write_log(error_fname,saved_query,error_string)

        pass

    

        #return response

def create_queries_by_year(vaultservice, exception_matter, config, matter_name, query_name, query_id):  

    query_list = []
    
    exception_matter_id = exception_matter['matterId']
    
    matter = get_matter(vaultservice, matter_name)
    matter_id = matter['matterId']
           
    query_body = get_query(vaultservice, matter_id, query_id)
    
    #print("query_body=", query_body)

    # first, pull this list of years from the config file
    years = config['years']
    
    # now for each query, we need to make a set of 
    # new ones broken down by each year, and store them
    # in a different matter
    
    for count, year in enumerate(years) :

        new_query = map_queryrow_year(matter_name, query_body, year)
         
        response = create_saved_query(vaultservice, exception_matter_id, new_query)
        
        if(response == None):
            print("error, empty response from create_saved_query")
            continue
        
        #print("response=", response)
        
        query_list += [new_query]


    return query_list
    
def create_query_by_timeslot( vaultservice, matter, final_search, timeslot):

    # create the query body
    
    # create the query


    return result
    

    
def get_queries ( service, matter_id ) :

    token = "1"
    token_count = 0
    queries = []
    
    while(token):

        if(token=="1"):
            token=""
            
        results = service.matters().savedQueries().list(matterId=matter_id,pageSize=10000, pageToken=token).execute()
        
        token = results.get('nextPageToken')
        #print ("token=", token)
        token_count += 1
        #print("token_count", token_count)                     
        
        queries += results.get('savedQueries',[])


    return queries

    
#******************
# Manage Exports
#******************

    
def create_export(service, matter_id, export_type, querybody):

    #todo add paramater for query options
    mail_query_options = {'excludeDrafts': True}

    # get the export name from the query wrapper
    export_name = querybody.get('displayName')

    # pull the query from inside the wrapper
    query = querybody.get('query')
    
    # pull the paramaters from the query needed to form the 
    # export creation
    
    corpus = query.get('corpus')
    dataScope = query.get('dataScope')
    searchMethod = query.get('searchMethod')
   
    
    accountInfo = query.get('accountInfo')
    orgUnitInfo = query.get('orgUnitInfo')
    terms = query.get('terms')
    startTime = query.get('startTime')
    endTime = query.get('endTime')
    mailOptions = query.get('mailOptions')
    method = query.get('method')
    
    
    # build the export request
    
    if(accountInfo != None):
    
        mail_query = {
            'corpus': corpus,
            'dataScope': dataScope,
            'searchMethod': searchMethod,
            'accountInfo': accountInfo,
            'terms': terms,
            'startTime' : startTime,
            'endTime' : endTime,
            'mailOptions':mailOptions,
            'method':method
            }
    
    if(orgUnitInfo != None):
    
        mail_query = {
            'corpus': corpus,
            'dataScope': dataScope,
            'searchMethod': searchMethod,
            'orgUnitInfo': orgUnitInfo,
            'terms': terms,
            'startTime' : startTime,
            'endTime' : endTime,
            'mailOptions':mailOptions,
            'method':method
            }
        
    mail_export_options = {
        'exportFormat': export_type, 
        'showConfidentialModeContent': True
        }
        
    wanted_export = {
        'name': export_name,
        'query': mail_query,
        'exportOptions': {
        'mailOptions': mail_export_options
        }
    }
    export = service.matters().exports().create(
        matterId=matter_id, body=wanted_export).execute()
        
    
    return export



def run_exports(vaultservice, matter_id, export_type, export_queue_length):

    export_in_progress = "IN_PROGRESS"
    export_completed = "COMPLETED"
    export_failed = "FAILED"
    
    global export_count
    global query_count
    global num_queries
    global num_exports
    
    
    total_queries = 0
         
    # Call the Vault API
    
    matter = get_matter_byid(vaultservice, matter_id)
    
    if(matter == None):
        print("error, invalid matter")
        return None
    
    print("matter=",matter)
    matter_id = matter.get('matterId')
    print("matter_id=",matter_id)

    export_list = [] 

    queries = get_queries ( vaultservice, matter_id )
    
    if( queries == None) :
        print("error, no queries")
        return None
    
    
    num_queries = len(queries)
    num_exports = 0
    export_count = 0
    
    
    
    for query_count, query in enumerate(queries):

       
        total_count = reprocess_saved_query(vaultservice, matter, query)
    
        
        total_queries +=1
        
        set_query_count(query_count+1)
        
        print("query_num=", query_count," total_count=", total_count)
        
        if(total_count == None):
            count = 0
        else:
            count = int(total_count)
        
        if(count <= 0) :
            # count is zero, or there was an error so skip this query
            continue
        
        num_exports += 1
        
        # add the export to the queue if there is room
        
        time.sleep(30)
        
        export =  create_export(vaultservice, matter_id, export_type, query)
                    
        export_list += [export]
            
        while ( len(export_list) > export_queue_length):
        
        
            print("export_list length=", len(export_list) )
          
            time.sleep(60)
            
            for export in export_list :
            
                export_id       = export.get('id')
                export_name     = export.get('name')
                
                # get the status from operation
                export_status = get_export_status(vaultservice, matter_id, export_id)
                print("export_name=", export_name)
                print("export_status=", export_status)
                
                if(export_status == export_completed) :
                    # remove this export from the list
                    
                    export_list.remove(export)
                    export_count +=1
                    
                    
    while ( len(export_list) > 0):
    
        time.sleep(30)
        
        for export in export_list :
            export_id       = export.get('id')
            export_name     = export.get('name')
            export_status = get_export_status(vaultservice, matter_id, export_id)
            #print("export_name=", export_name)
            if(export_status == export_completed) :
                # remove this export from the list
                export_list.remove(export)
                export_count +=1
    
    print("length of export queue=", len(export_list) )
    
    exports = get_exports(vaultservice, matter_id)
    
    return exports

        

def get_export_status(vaultservice, matter_id, export_id) :

    export = vaultservice.matters().exports().get(matterId=matter_id, exportId=export_id).execute()
    
    status = export.get('status')
    
    return status
    
    
def delete_export(vaultservice, matter_id, export_id):
 
    response = vaultservice.matters().exports().delete(matterId=matter_id, exportId=export_id).execute()
    
    return response
    
def get_exports(vaultservice, matter_id):

        exports = []
        # get list of exports
        
        token = "1"
        
        while (token != "") :
        
            if( token== "1") :
                token = ""

            results = vaultservice.matters().exports().list(matterId=matter_id, pageSize=100000, pageToken=token).execute()

            print("results=", results)
            print("token=", token)
            
            # get the list of exports associated with this matter
            exports += results.get('exports',[])
            print("num exports=", len(exports))
    
        return exports



#******************
# User routines
#******************

def add_collaborator(service, matter_id, account_id):

    print("account_id=", account_id)

    request = {  "matterPermission" : { "accountId" : account_id,
                                        "role": "COLLABORATOR"},
                                        "sendEmails" : False,
                                        "ccMe" : False }
              
                                        
    permission = service.matters().addPermissions(matterId=matter_id, body=request ).execute()
    
    print("permission=", permission)
    #permission = service.matters().addPermissions(request).execute()

    return permission



def get_user(service, username):

    results = service.users().get(userKey=username).execute()
    
    #print(results)

    return results


def list_users(service) :

    users = []
    token=""

    #while (token != ""):
    #results = service.users().list(customer='my_customer',pageToken=token,maxResults=500).execute()
    results = service.users().list(domain="lacity.org",pageToken=token,maxResults=500).execute()

    users += results.get('users',[])
    
    token = results.get('nextPageToken')
    
    print("token=", token)
    print("results=", results)

    num_calls = 0


    while (token != ""):
        time.sleep(1)
        #results = service.users().list(customer='my_customer',pageToken=token,maxResults=500).execute()
        results = service.users().list(domain="lacity.org",pageToken=token,maxResults=500).execute()
        token = results.get('nextPageToken')
        print("token=", token)
        print("results=", results)
        num_calls += 1
        users += results.get('users',[])
        print("num_calls=", num_calls)

        print("num users=", len(users))


    handle = open("users.csv", 'w' )

    for user in users:
        email = user.get('primaryEmail')
        handle.write('"'+email+'"'+'\n')

    handle.close()
        
    #users += results.get('users',[])
    #users = results['users']    

    return users
    

#******************
# Org Unit routines
#******************

def list_org_units(service) :
            
    # Call the Admin SDK Directory API
    
    depts = []
    
    results = service.orgunits().list(customerId='my_customer').execute()
    orgunits = results.get('organizationUnits', [])
    
    for org in orgunits :
        #print("parent=",org['name'], org['orgUnitId'])
        depts += [['parent-org',org['name'],org['orgUnitId']]]
        time.sleep(.1)
        results = service.orgunits().list(customerId='my_customer',orgUnitPath=org['name']).execute()
        sub_orgunits = results.get('organizationUnits', [])
        for sub_org in sub_orgunits:
            #print(sub_org['name'],sub_org['orgUnitId'])
            depts += [['sub-org',sub_org['name'],sub_org['orgUnitId']]]
            try:
                # sub of the sub
                #print("sub_org=", sub_org)
                time.sleep(.1)
                results = service.orgunits().list(customerId='my_customer',orgUnitPath=sub_org['orgUnitPath']).execute()
                #print("results=", results)
                
                sub_sub_orgunits = results.get('organizationUnits', [])
                for sub_sub_org in sub_sub_orgunits:
                    #print(sub_org['name'],sub_org['orgUnitId'])
                    depts += [['sub-sub-org',sub_sub_org['name'],sub_sub_org['orgUnitId']]]
            except: 
                pass
        
        

    
    return depts


    


def get_orgid(service, orgname) :
            
    # Call the Admin SDK Directory API
    
    results = service.orgunits().list(customerId='my_customer').execute()
    orgunits = results.get('organizationUnits', [])
    
    for org in orgunits :
    
        if(org['name'] == "lacity.gov Departments"):
        
            results = service.orgunits().list(customerId='my_customer',orgUnitPath=org['name']).execute()
            sub_orgunits = results.get('organizationUnits', [])
            
            for sub_org in sub_orgunits:
                if(orgname == sub_org['name']):
                    #print(sub_org)
                    return sub_org['orgUnitId']
                
    return None


#**************************
#  operation trace wrappers
#**************************


def operation_request(service, matter, request, query) :
    global trace_fname
    total_queries = get_num_queries()
    
    matter_id = matter.get('matterId')
    
    api_trace(matter, query, "service.matters().count():before:", service, request, total_queries)
    operation = service.matters().count(matterId=matter_id, body=request).execute()   
    api_trace(matter, query, "service.matters().count():after:", service, operation, total_queries)
    
    return operation
    
def operation_read(service, matter, operation, query):
    global trace_fname
    total_queries = get_num_queries()

    matter_id = matter.get('matterId')

    api_trace(matter, query, "service.operations().get():before:", service, operation, total_queries)
    operation = service.operations().get(name=operation.get('name')).execute()
    api_trace(matter, query, "service.operations().get():after:", service, operation, total_queries)

    return operation



#**************************
#  data validation routines
#**************************

def clean_search_name(value) :
    
        
    temp = str(value).replace("[","")
    temp1 = temp.replace("]","")
    temp = temp1.replace('“','"')
    temp1 = temp.replace('”','"')
    temp = temp1.replace("'","")
    temp1 = temp.replace('""','"')
    temp = temp1.replace(' ','')


    return temp   

def clean_search_string(value) :

    temp = str(value).replace("[","")
    temp1 = temp.replace("]","")
    temp = temp1.replace('“','"')
    temp1 = temp.replace('”','"')
    temp = temp1.replace("'","")
    temp1 = temp.replace('""','"')

    return temp1   

def remove_quotes (string) :
    temp = str(string).replace('"','')

    return temp
    


###  vault exports ###



def vault_matter_tocsv(vaultservice, config, matter_name, csv_name):
        
        
        # configure vault API trace
        configure_vault_api(config, matter_name)
    
        #configure the api trace_fname
    
        configure_trace_api(config, matter_name)
        
    
        matter = get_matter(vaultservice, matter_name)
        
        matter_name = matter['name']
        
        if (matter == None):
            print("invalid matter")
            exit()
        
        matter_id = matter['matterId']
        
        
 		
		# get the queries from the vault matter
		# into a list
                
        queries =  get_queries(vaultservice, matter_id)
        
        print("len of queries=", len(queries) )
        
        csv_handle = open(csv_name, 'a+' )

        
        for query in queries :
        
            #print("query=", query)
            #exit()
            
         
        #the following fields are from the VAULT query body
            savedQueryId    = query['savedQueryId']
            displayName     = query['displayName']
            query_data      = query['query']
            corpus          = query_data['corpus']
            dataScope       = query_data['dataScope'] 
            searchMethod    = query_data['searchMethod']
            terms           = query_data['terms']
            startTime       = query_data['startTime'] 
            endTime         = query_data['endTime']
            timeZone        = query_data['timeZone']
            method          = query_data['method']
            matterId        = query['matterId']
            createTime      = query['createTime']
            
            
            # these fields to be updated when the
            # count file is merged in
            # disposition 
            # qa_status
            # count result
                       
            row = '"' + matter_name      + '"' + ','  + \
                  '"' + matterId        + '"' + ','  + \
                  '"' + displayName     + '"' + ',' +  \
                  '"' + savedQueryId    + '"' + ','  + \
                  '"' + startTime       + '"' + ','  + \
                  '"' + endTime         + '"' + ','  + \
                  '"' + timeZone        + '"' + ','  + \
                  '"' + method          + '"' + ','  + \
                  '"' + createTime      + '"' + ','  + \
                  '"' + '"' + ',' + \
                  '"' + '"' + ',' + \
                  '"' + '"'  + '\n'   
                  
                  
            
            # append the row to the .csv file
            csv_handle.write(row)
            
        
        csv_handle.close()
        
