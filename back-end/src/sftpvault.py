import pysftp
from urllib.parse import urlparse
import os
import sys 
import time
from datetime import datetime


class Sftp:
    def __init__(self, hostname, username, password, port=22):
    
        """Constructor Method"""
        if (password == ""):
            password = "None"
        
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self, key_file):
        """Connects to the sftp server and returns the sftp connection object"""

        try:
            # Get the sftp connection object
            
            print("password=", self.password)
            if(self.password == "None"):
            
                self.connection = pysftp.Connection(
                    host=self.hostname,
                    username=self.username,
                    #password=self.password,
                    port=self.port,
                    private_key=key_file,
                    )
            else:
                self.connection = pysftp.Connection(
                    host=self.hostname,
                    username=self.username,
                    #password=self.password,
                    port=self.port,
                    private_key=key_file,
                    private_key_pass=self.password,
                    )
            
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {self.hostname} as {self.username}.")

    def disconnect(self):
        """Closes the sftp connection"""
        self.connection.close()
        print(f"Disconnected from host {self.hostname}")

    def listdir(self, remote_path):
        """lists all the files and directories in the specified path and returns them"""
        for obj in self.connection.listdir(remote_path):
            yield obj

    def listdir_attr(self, remote_path):
        """lists all the files and directories (with their attributes) in the specified path and returns them"""
        for attr in self.connection.listdir_attr(remote_path):
            yield attr
    
    
    
    def directory_exists(self, path, dirname):

        directoryExists = False
        
        for file in self.listdir_attr(path):
            if(file.filename == dirname):
                directoryExists = True
            
        if(directoryExists == True):
            print("directory exits")
        else:
            print("directory does not exist")
            self.connection.makedirs(dirname)  
            
        return directoryExists
    

    def download(self, remote_path, target_local_path):
        """
        Downloads the file from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """

        try:
            print(
                f"downloading from {self.hostname} as {self.username} [(remote path : {remote_path});(local path: {target_local_path})]"
            )

            # Create the target directory if it does not exist
            path, _ = os.path.split(target_local_path)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception as err:
                    raise Exception(err)

            # Download from remote sftp server to local
            self.connection.get(remote_path, target_local_path)
            print("download completed")

        except Exception as err:
            raise Exception(err)
    

    def upload(self, source_local_path, remote_path):
        """
        Uploads the source files from local to the sftp server.
        """

        try:
            print(
                f"uploading to {self.hostname} as {self.username} [(remote path: {remote_path});(source local path: {source_local_path})]"
            )

            # Download file from SFTP
            self.connection.put(source_local_path, remote_path)
            print("upload completed")

        except Exception as err:
            raise Exception(err)

def vault_tosftp(matter_id, matter_name, log_dir, sftp_url, sftpPassword, key_file):
    
    
    parsed_url = urlparse(sftp_url)
    
    #
    ####    TODO:   setup host keys with a general 
    #               settings action menu
    #
    #cnopts = pysftp.CnOpts(knownhosts='known_hosts')
    #cnopts.hostkeys.load("ext_jeffrey_goodwin-nopass")
    print("parsed_url=",parsed_url);
    print("parsed password=",parsed_url.password)
    

    sftp = Sftp(
        hostname=parsed_url.hostname,
        username=parsed_url.username,
        password=sftpPassword)
        #password=parsed_url.password)

    
    # Connect to SFTP
    sftp.connect("../sftp-keys/"+key_file)


    # Lists files with attributes of SFTP
    ### TEMP, TODO: put in general settings or get on login
    path = "/home/ext_jeffrey_goodwin"
    
    print(f"List of files with attributes at location {path}:")
    for file in sftp.listdir_attr(path):
        print(file.filename, file.st_mode, file.st_size, file.st_atime, file.st_mtime)
    #
    #### make the high level directories
    #
    now = datetime.now()
    nowstr = now.strftime("%Y-%m-%d, %H:%M:%S")
    matter_path = matter_name
    
    if(sftp.directory_exists(path,matter_name)==True):
        matter_path = matter_name + '--' + nowstr
        sftp.directory_exists(path,matter_path)
        
    sftp.directory_exists(path,matter_path+'/'+'downloads')
    sftp.directory_exists(path,matter_path+'/'+'mbox')    
    
    #
    #### current home directory
    #
    
    remote_home_directory = sftp.connection.pwd
    print("remote_home_directory=", remote_home_directory)
    
    # current directory
    curdir = os.getcwd()
    print("curdir=",curdir)
    
    ## open file for logging
    log_file = matter_name + "-sftp-transfer-log.csv"
    handle = open(log_dir + "\\" + log_file, 'w' )
    
    #
    #### Iterate through the local files
    #
    local_path = os.getcwd()
    local_home_path = os.getcwd() + '\\' + matter_id
    os.chdir(local_home_path)
    
    # get a list of the current directories
    dirs = os.scandir()
    
    # current directory
    curdir = os.getcwd()
    print("curdir=",curdir)
    
    dir_count = 0
    file_count = 0
    
    for directory in dirs:
    
        # upload vault extracts
        
        if(directory.name == "downloads"):
            
            os.chdir(curdir+'\\'+directory.name)
            subdirs = os.scandir()
            
            for subdir in subdirs:
            
                if(subdir.is_file() == True):
                    continue
                 
                target_remote_path = matter_path+'/'+directory.name+'/'+subdir.name
                source_local_path  = curdir+'\\'+directory.name+'\\'+subdir.name;
                
                sftp.directory_exists(path,target_remote_path)
                
                sftp.connection.chdir(target_remote_path)

                result = sftp.connection.put_d(source_local_path, '', preserve_mtime=True)
                
                sftp.connection.chdir(remote_home_directory)
                
                
                
                files = os.scandir(subdir)
                for file in files:
                    entry = '"'+file.name+'"'+ ',' +       \
                            '"'+datetime.now().strftime("%Y-%m-%d,%H:%M:%S") + '"' + '\n'
                    handle.write(entry)
    
        if(directory.name == "work"):
        
                target_remote_path = matter_path+'/'+'mbox'
                source_local_path  = curdir+'\\'+directory.name+'\\'+'mbox'
        
                sftp.directory_exists(path,target_remote_path)
                
                sftp.connection.chdir(target_remote_path)
                
                result = sftp.connection.put_d(source_local_path, '', preserve_mtime=True)
                
                sftp.connection.chdir(remote_home_directory)
                
                files = os.scandir(source_local_path)
                for file in files:
                    entry = '"'+file.name+'"'+ ',' +       \
                            '"'+datetime.now().strftime("%Y-%m-%d,%H:%M:%S") + '"' + '\n'
                    handle.write(entry)
    
    print(f"List of files at location {path}:")
    print([f for f in sftp.listdir(path)])

    # Close the log file
    handle.close()
    # Disconnect from SFTP
    sftp.disconnect()
    return log_file