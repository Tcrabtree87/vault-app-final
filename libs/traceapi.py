
from datetime import datetime
import time


# api logging wrappers
#
#
trace_fname = ""
trace_dir = ""

def configure_trace_api(config, matter_name, tracedir) :

    global trace_fname
    global trace_dir

    trace_fname = tracedir + '\\' + matter_name + config['apiFname']            #"-api.csv"
    trace_dir = tracedir


# api_trace

def api_trace (matter, query, api_descriptor, service, operand, total_queries):
    global trace_fname
    global trace_dir
    
    query_name = query.get('displayName')
    query_id = query.get('savedQueryId')
    matter_id = matter.get('matterId')
    matter_name = matter.get('name')
    
    #'"'+str(total_queries)+'"'+','+ \
    
    log_handle = open(trace_fname,'a+' )
    log_handle.write(   '"'+str(matter_id)+'"'+','+ \
                        '"'+str(query_name)+'"'+','+ \
                        '"'+str(query_id)+'"'+','+ \
                        '"'+api_descriptor+'"'+','+ \
                        '"'+str(service)+'"'+','+ \
                        '"'+str(datetime.now())+"-"+str(time.time())+'"'+','+ \
                        '"'+str(operand)+'"'+'\n')
    log_handle.close()
    return


def remove_quotes (string) :
    temp = str(string).replace('"','')
 
    return temp
   
max_cell_size = 32767

def write_log(fname,query_body,log_string):
    global max_cell_size
    global trace_fname
    global trace_dir
    
    query = query_body.get('query')
    query_id = query_body.get('savedQueryId')
    query_name = query_body.get('displayName')
    
    #if(len (log_string) > max_cell_size):
    #    temp = remove_quotes(log_string)
    ##    log_string=temp
        # it won't fit in a single cell, so we need to break it up  
    #    log_handle = open(fname,'a+' )
        #first write out the header
    #    log_handle.write('"'+query_name+'"'+','+'"'+str(query_id)+'"'+','+'"'+str(datetime.now())+':'+str(time.time())+'"')
        #now write out each chunk
    #    total_length = len(log_string)
    #    start_point = 0
    #    remainder = len(log_string) # - max_cell_size
    #    chunk_size = max_cell_size
        
        #log_handle.write('"'+str[0:32766]+'"'+',')
    #    chunk_count = 0
        
        #while (remainder > 0):
        #    chunk_count +=1
        #    
        #    log_handle.write(','+'"'+log_string[start_point:start_point+chunk_size]+'"')
        #    
        #    remainder -= chunk_size
        #    start_point += chunk_size-1
        #    if(remainder < max_cell_size):
        #        chunk_size = remainder
        #    else:
        #        chunk_size = remainder - max_cell_size
        #        
        #        
        #log_handle.write('\n')
        #log_handle.close()
        #return    
    #print("trace_dir=", trace_dir, " ", fname)
    trace_file_name = trace_dir + '\\' + fname
    #print("trace_file_name=", trace_file_name)
    log_handle = open(trace_file_name,'a+' )
    log_handle.write('"'+query_name+'"'+','+'"'+str(query_id)+'"'+','+'"'+str(datetime.now())+':'+str(time.time())+'"'+','+ str(log_string)+'\n')
    log_handle.close()

    return

def write_error(fname, log_string):

    global trace_dir
    global max_cell_size
    
    if(len (log_string) > max_cell_size):
        temp = remove_quotes(log_string)
        log_string=temp
        # it won't fit in a single cell, so we need to break it up  
        log_handle = open(trace_dir+'\\'+fname,'a+' )
        #first write out the header
        #log_handle.write('"'+query_name+'"'+','+'"'+str(query_id)+'"'+','+'"'+str(datetime.now())+':'+str(time.time())+'"')
        log_handle.write('"'+str(datetime.now())+':'+str(time.time())+'"')
        #now write out each chunk
        total_length = len(log_string)
        start_point = 0
        remainder = len(log_string) # - max_cell_size
        chunk_size = max_cell_size
        
        #log_handle.write('"'+str[0:32766]+'"'+',')
        chunk_count = 0
        
        while (remainder > 0):
            chunk_count +=1
            
            log_handle.write(','+'"'+log_string[start_point:start_point+chunk_size]+'"')
            
            remainder -= chunk_size
            start_point += chunk_size-1
            if(remainder < max_cell_size):
                chunk_size = remainder
            else:
                chunk_size = remainder - max_cell_size
                
                
        log_handle.write('\n')
        log_handle.close()
        return    

    log_handle = open(trace_dir+'\\'+fname,'a+' )
    log_handle.write('"'+str(datetime.now())+':'+str(time.time())+'"'+','+ str(log_string)+'\n')
    log_handle.close()

    return


#
#
# end api loggging wrappers
