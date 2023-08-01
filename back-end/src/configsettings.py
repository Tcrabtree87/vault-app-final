
import os
import json

#    
####  this is for matter configuration file
#    

def get_matter_config (matter_id, data_dir):

    matter_config = {}
        
    matter_config_fname = data_dir + matter_id +".json"
    
    with open(matter_config_fname) as f:
        data = f.read()
        
    # reconstructing the data as a dictionary
    matter_config = json.loads(data)
            
    print("matter_config=", matter_config)

    return matter_config


def update_matter_config (matter_id, data_dir, matter_config):

    #matterConfig = json.loads(matter_config)
   
    # write it out to a file
    # reformat matter_config, and store in .json file with
    # with matter_id as file name
    
    config_data = json.dumps(matter_config,indent=2)

    matter_config_fname = data_dir + matter_id +".json"
    
    handle = open(matter_config_fname,'w+' ) # overwrites the file
    handle.write(config_data)
    handle.close()
    
    return config_data

#
####  this is for the general configuration file
#
 
async def update_my_settings (config, creds, settings):
    
    #vaultservice = build('vault', 'v1', credentials=creds)
    
    print("settings=", settings)
    
    config_fname = 'config.json'
    
    new_config = settings['settingsParms']
    
    #settingsParms : { 		"powerUser" : power_user,
	#						"sftpUsername" : sftp_user,
	#						"logFiles" : log_files,
	#						"dataFiles" : data_files,
	#						"sftpIP" : sftp_ip,
	#						"sharedDrive" : shared_drive,
	#						"exportQueueLimit" : queue_limit
    
    config['powerUser']         = new_config['powerUser']
    config['sftpUsername']      = new_config['sftpUsername']
    config['sftpPassword']      = new_config['sftpPassword']
    config['logFiles']          = new_config['logFiles']
    config['dataFiles']         = new_config['dataFiles']
    config['sftpIP']            = new_config['sftpIP']
    config['sharedDrive']       = new_config['sharedDrive']
    config['exportQueueLimit']  = new_config['exportQueueLimit']
    
    # the config file has already been read in
    # and is a global variable in the main process_tree
    # We need to update it with the new settings
    
    # and write it back out to the persistent configuration
    # file
    
    # write it out to a file
    # reformat matter_config, and store in .json file with
    # with matter_id as file name
    
    config_data = json.dumps(config, indent=2)

    print("config_data=", config_data)
    
    handle = open(config_fname,'w+' ) # overwrites the file
    handle.write(config_data)
    handle.close()
    
    new_config = json.loads(config_data)
    
    return new_config
    
    
        
