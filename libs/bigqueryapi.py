import time
from datetime import datetime

from googleapiclient.errors import HttpError

from traceapi import *


def list_datasets(bigquery_client):

    # now list the tables just created in the dataset
    datasets = list(bigquery_client.list_datasets())  # Make an API request.
    project = bigquery_client.project

    if datasets:
        print("Datasets in project {}:".format(project))
        for dataset in datasets:
            
            print("\t{}".format(dataset.dataset_id))
            print(dataset)
            
            table_blobs = bigquery_client.list_tables(dataset)  # Make an API request.
            tables = list(table_blobs)
            
            print("Tables contained in '{}':".format(dataset))
            
            for table in tables :
                print(table.table_id)
                             
    else:
        print("{} project does not contain any datasets.".format(project))

def config_job(bigquery):

    jobConfig = bigquery.LoadJobConfig()
    jobConfig.skip_leading_rows = 0
    jobConfig.source_format = bigquery.SourceFormat.CSV
    jobConfig.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE   
    jobConfig.autodetect=False
    
    return jobConfig


def merge_counts(bigquery_client, config, vaultTableName, countsTableName):

    csvName = config['countsCsvFile']
    project = bigquery_client.project


    datasetName = config['datasetName']
    
    
    countsTableRef = project + "." + datasetName + "." + countsTableName
    vaultTableRef = project + "." + datasetName + "." + vaultTableName

    query_part1 = "MERGE " + vaultTableRef + " V" + "\n"
    query_part2 = "USING (SELECT * FROM " + countsTableRef + " ) C"  + "\n"
    query_part3 = "ON V.savedQueryId = C.savedQueryId"  + "\n"
    query_part4 = "WHEN MATCHED THEN"  + "\n"
    query_part5 = "    UPDATE SET count =   C.count, "  + "\n"
    query_part6 = "                         qa_status = 'counted' "
    
    query = query_part1 + query_part2 + query_part3 + query_part4 + query_part5  + query_part6 
    #print("query=", query)
                      
    query_job = bigquery_client.query(query)  # Make an API request.
    
    result = query_job.result()
    
    total_rows = 0
    
    for row in result:
        total_rows +=1
    
    return total_rows
    
    
def load_csv_table(bigquery_client, config, jobConfig, csvName, tableId):    
      
        datasetName = config['datasetName']
        
        tableRef = bigquery_client.dataset(datasetName).table(tableId)
        
        print(tableRef)
        
        with open(csvName, "rb") as source_file:
            bigqueryJob = bigquery_client.load_table_from_file(source_file, tableRef, job_config=jobConfig)

        bigqueryJob.result()
            
        print("tableRef=",tableRef)
            
        table = bigquery_client.get_table(tableRef)
            
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), tableRef
            )
        )
        return table


def make_table(bigquery, bigquery_client, config, tableId, jobConfig ):


    # now we need to create a table
    # with the name of the matter, for run1 and run2
        
    #from google.cloud import bigquery
        
   
    
    datasetName = config['datasetName']
    #tableId = matter_name #+ "_" + run.name
    #tableId = tableId.replace("-","_")
    #tableId = tableId.replace(".","_")
        
    tableRef = bigquery_client.dataset(datasetName).table(tableId)
    print(tableRef)
        
    table = bigquery.Table(tableRef, schema=jobConfig.schema)
    print("table=", table)
    master_table = bigquery_client.create_table(table)  # Make an API request.
    print("master_table=", master_table)
    print("Created master_table {}.{}.{}".format(master_table.project, master_table.dataset_id, master_table.table_id))

    return table


            
def make_vault_table(bigquery, bigquery_client, config, matter_name, run_dir):
    
    jobConfig = config_job(bigquery)
        
    jobConfig.schema = [
                        
                        #the following fields are from the VAULT query body
                        bigquery.SchemaField("matter_name", "STRING"),                           
                        bigquery.SchemaField("matterId", "STRING"),
                        bigquery.SchemaField("displayName", "STRING"),
                        bigquery.SchemaField("savedQueryId", "STRING"),
                        #bigquery.SchemaField("terms", "STRING"),
                        bigquery.SchemaField("startTime", "STRING"),
                        bigquery.SchemaField("endTime", "STRING"),
                        
                        bigquery.SchemaField("timeZone", "STRING"),
                        bigquery.SchemaField("method", "STRING"),
                        bigquery.SchemaField("createTime", "STRING"),
                        
                        # this fields are used for  Q/A
                        bigquery.SchemaField("disposition", "STRING"),
                        bigquery.SchemaField("qa_status", "STRING"),
                        # these fields can be updated when the count is
                        # updated
                        bigquery.SchemaField("count", "INTEGER")
                        ]

    
    tableId = matter_name + "_" + run_dir
    tableId = tableId.replace("-","_")
    tableId = tableId.replace(".","_")
        
    
    table = make_table(bigquery, bigquery_client, config, tableId, jobConfig )
    
    return table
    
    
def make_counts_table(bigquery, bigquery_client, config, matter_name, run_dir):
    
    jobConfig = config_job(bigquery)
        
    jobConfig.schema = [
                            
                            #the following fields are from the VAULT query body
                            bigquery.SchemaField("matter_name", "STRING"),                           
                            bigquery.SchemaField("matterId", "STRING"),
                            bigquery.SchemaField("displayName", "STRING"),
                            bigquery.SchemaField("savedQueryId", "STRING"),
                            bigquery.SchemaField("count", "INTEGER")
                            ]

    
    tableId = matter_name + "_REGEN_COUNTS_" + run_dir
    tableId = tableId.replace("-","_")
    tableId = tableId.replace(".","_")
        
    
    table = make_table(bigquery, bigquery_client, config, tableId, jobConfig )
    
    return table
    
    
def make_error_table(bigquery, bigquery_client, config, matter_name, run_dir):
    
    jobConfig = config_job(bigquery)
        
    jobConfig.schema = [
                            #the following fields are from the VAULT query body
                            bigquery.SchemaField("matter_name", "STRING"),                           
                            bigquery.SchemaField("matterId", "STRING"),
                            bigquery.SchemaField("displayName", "STRING"),
                            bigquery.SchemaField("savedQueryId", "STRING"),
                            bigquery.SchemaField("count", "INTEGER")
                            ]

    
    tableId = matter_name + "_ERROR_COUNTS_" + run_dir
    tableId = tableId.replace("-","_")
    tableId = tableId.replace(".","_")
        
    
    table = make_table(bigquery, bigquery_client, config, tableId, jobConfig )
    
    return table