        
  
#
#   Author:  Jeffrey Goodwin
#   Date: 6/5/2022
#   GOOGLE Drive API wrapper routines
#   

  
##
# Google Drive and Folder Operations
##
       
        

def find_shared_drives (service) :

    result = service.drives().list().execute()
    print("result=",result)
    drives = result.get('drives')
    print("drives",drives)
    for drive in drives :
        name = drive.get('name')
        print("name=",name)
        drive_id   = drive.get('id')
        print("drive_id=",drive_id)
    
        if(name == 'Google Apps eDiscovery') :
            return drive
            
    return None

def find_file(service, drive, parent, filename):
     
    page_token = ""

    print("in find file, filename = ", filename)
    
    name = "'" + filename + "'"
    
    print("in find file, name = ", name)

    
    query = "mimeType : 'application/vnd.google-apps.spreadsheet' and name :" + name
    
    file = service.files().list(  q=query,
                                    includeItemsFromAllDrives=True,
                                    supportsAllDrives=True,
                                    #useDomainAdminAccess=True,
                                    spaces='drive',
                                    fields='nextPageToken, files( id, name)',
                                    pageToken=page_token).execute() 
                                    
    
    return file
    

def find_folder(service, drive, foldername):
     
    page_token = ""
    print("drive=",drive)
    
    query = "mimeType : 'application/vnd.google-apps.folder' and name=" + foldername
    print("q=",query)
        
     
    folder = service.files().list(  q=query,
                                    includeItemsFromAllDrives=True,
                                    supportsAllDrives=True,
                                    #useDomainAdminAccess=True,
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=page_token).execute() 
    
    
    
    return folder
    
##
# END - Google Drive and Folder Operations
##
   
    
