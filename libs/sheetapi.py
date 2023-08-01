
from googleapiclient.errors import HttpError

from dataclasses import dataclass


#
#   Author:  Jeffrey Goodwin
#   Date: 6/5/2022
#   GOOGLE Sheet API wrapper routines
#   

##
# Google Sheet Operations
##

def set_values(sheetservice, sheet_id, query_range, values) :

        value_input_option =    "USER_ENTERED"


        # format values
        formatted_values = [
                    [
                    values,  #'Search Name', 'Counts',   # Cell values ...
                    ],
                # Additional rows ...
                ]

   
        # Call the Sheets API
 
        body = {
            'values': formatted_values 
        }
        
        try:
        
            result = sheetservice.spreadsheets().values().update(
                                                        spreadsheetId=sheet_id, 
                                                        range=query_range,
                                                        valueInputOption=value_input_option, 
                                                        body=body).execute()
            
            print(f"{result.get('updatedCells')} cells updated.")
        
            return result
        
        except HttpError as error:
            
            print(f"An error occurred: {error}")
            return error





def get_values(sheets, sheet_id, query_range) :

   
    # Call the Sheets API
 
    result = sheets.values().get(spreadsheetId=sheet_id,
                                range=query_range).execute()
 
    values = result.get('values', [])
 
        
    return values


def create_sheet(drives, service, parent, sheetname) :

    folder = parent.get('files',[])

    parent_folder = folder.pop()
    parent_id = parent_folder.get('id')
    print("parent_id=",parent_id)


    file_metadata = {
        'parents' : [parent_id],
        'name': sheetname,
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    
    file = service.files().create(body=file_metadata,
                                  supportsAllDrives=True,
                                  fields='id').execute()
                                  
    print ('Sheet ID: %s' % file.get('id'))
       
    return file
    
    

def get_tab_values(sheets, sheet_id, tab_name):

# Call the Sheets API
    print("sheet_id=",sheet_id)
    result = sheets.values().get(spreadsheetId=sheet_id,
                                range=tab_name).execute()
 
    values = result.get('values', [])
    #print(values)
        
    return values



def get_sheet(sheets, file, query_range) :


    sheetlist  = file.get('files',[])
    sheet = sheetlist.pop()
    sheet_id = sheet.get("id")
    
    
    # Call the Sheets API
    print("sheet_id=",sheet_id)
    result = sheets.values().get(spreadsheetId=sheet_id,
                                range=query_range).execute()
 
    values = result.get('values', [])
        
    return values
    
    
    

# load the .csv file into the specified sheet_id, into the tab 
# at the desired location





def load_csv(service, csv_path, sheet_id, tab_id):

    response = {}
    
    print("in load_csv, tab_id=", tab_id)
    
    try:
    
        with open(csv_path, 'r') as csv_file:
            csvContents = csv_file.read()
        body = {
            'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": tab_id, #"Sheet1", #sheet_id,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0", # adapt this if you need different positioning
                },
                "data": csvContents,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
                }
            }]
        }
        request = service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body)
        response = request.execute()
        
    except:

    #except HttpError as err:
        print("error loading csv file")
        response = None
        pass
        
        
    return response

    
    
    
    
    


 
def add_sheet_tab(service, sheet_id, tab_name):

    body = {
        'requests': [{
        'addSheet': {
        'properties': {
        'title': tab_name,
        'tabColor': {
                    'red': 0.44,
                    'green': 0.99,
                    'blue': 0.50
                    }
                }
            }
        }]
    }

    result = service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body=body).execute()
            
    return result
     
    
    
##
# End Google Sheet Operations
##
    

@dataclass
class SheetRange:
    startRowIndex       : int
    endRowIndex         : int
    startColumnIndex    : int
    endColumnIndex      : int
    
    
    def __init__(self, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex):
            
            self.startRowIndex = startRowIndex
            self.endRowIndex = endRowIndex
            self.startColumnIndex = startColumnIndex
            self.endColumnIndex = endColumnIndex

@dataclass
class CopyRange:
    sourceRange : SheetRange
    targetRange : SheetRange
    sheetId     : str
    sourceSheetId : int
    targetSheetId : int
    sheetservcie : {}
    batch_copy_paste          : {}

    def __init__(   self, 
                    sheetservice, 
                    sourceRange, 
                    targetRange, 
                    sheetId, 
                    sourceSheetId, 
                    targetSheetId):
    
            self.sheetservice = sheetservice
            self.sourceRange = sourceRange
            self.targetRange = targetRange
            self.sheetId = sheetId
            self.sourceSheetId = sourceSheetId
            self.targetSheetId = targetSheetId
    
    
    
            self.batch_copy_paste =   {
                    "requests": [
                    {
                    "copyPaste": {
                    "source": {
                    "sheetId": sourceSheetId,
                    "startRowIndex": sourceRange.startRowIndex,
                    "endRowIndex": sourceRange.endRowIndex,
                    "startColumnIndex": sourceRange.startColumnIndex,
                    "endColumnIndex": sourceRange.endColumnIndex,
                    },
                    "destination": {
                    "sheetId": targetSheetId,
                    "startRowIndex": targetRange.startRowIndex,
                    "endRowIndex": targetRange.endRowIndex,
                    "startColumnIndex": targetRange.startColumnIndex,
                    "endColumnIndex": targetRange.endColumnIndex,
                    },
                    "pasteType": "PASTE_NORMAL",
                    "pasteOrientation": "NORMAL"
                    }
                }
                ]
            }
        

@dataclass
class PasteValues:

    
    sourceRange : CopyRange
    copyText  : str
    copyRange : str
    paste_request : {}
    
    def __init__(self, sourceRange, copyRange, copyText):
    
   
        self.sourceRange = sourceRange
        self.copyText = copyText
        self.copyRange = copyRange
        
        #print("copyRange.sourceRange.startRowIndex=", copyRange.sourceRange.startRowIndex)
        #print("copyRange.sourceRange.endRowIndex=", copyRange.sourceRange.endRowIndex)
        
        
        
        
    def paste_values(self):

    
        # change below to a request format that
        # will contain the header data
        # A1            B1              C1              
        # Apartment     Search          Counts         
        
        value_input_option =    "USER_ENTERED"
        
        
        
        body = {
            'values': self.copyText 
        }
        
        try:
        
            result = self.sourceRange.sheetservice.spreadsheets().values().update(
                                                        spreadsheetId=self.sourceRange.sheetId, 
                                                        range=self.copyRange,
                                                        valueInputOption=value_input_option, 
                                                        body=body).execute()
            
            print(f"{result.get('updatedCells')} cells updated.")
        
            return result
        
        except HttpError as error:
            
            print(f"An error occurred: {error}")
            return error



@dataclass
class PasteFormula:

    
    copyRange : CopyRange
    paste_request : {}
    
    def __init__(self, copyRange):
    
        
        self.copyRange = copyRange
        
        print("copyRange.sourceRange.startRowIndex=", copyRange.sourceRange.startRowIndex)
        print("copyRange.sourceRange.endRowIndex=", copyRange.sourceRange.endRowIndex)

        self.paste_request = {
            "requests": [
                {
                "repeatCell": {
                "range": {
                "sheetId": copyRange.targetSheetId,
                "startRowIndex": copyRange.sourceRange.startRowIndex+1,
                "endRowIndex": copyRange.sourceRange.endRowIndex,
                "startColumnIndex": 0, #copyRange.sourceRange.startColumnIndex,
                "endColumnIndex": 1, #copyRange.sourceRange.endColumnIndex
                },
                "cell": {
                "userEnteredValue": {
                "formulaValue": '=left(B2,Find("--",B2)-1)'
                }
                },
                "fields": "userEnteredValue"
                }
            }
        ]
    }

    
    def paste_formula ( self ) : 
    
        print("entered copy_paste")
        request = self.copyRange.sheetservice.spreadsheets().batchUpdate(spreadsheetId=self.copyRange.sheetId, body=self.paste_request)
        print("request=", request)
        response = request.execute()
        print("response=", response)
        

@dataclass
class InsertColumn:

    copyRange : CopyRange
    insert_request : {}
    
    def __init__(self, copyRange):
    
        self.copyRange = copyRange
        

        self.insert_request = {
            "requests": [
            {
                "insertDimension": {
                    "range": {
                    "sheetId": copyRange.sourceSheetId,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 1
                    },
                "inheritFromBefore": False
                },
            }
            ],
        }

    def insert_column ( self ) : 
    
        print("entered copy_paste")
        request = self.copyRange.sheetservice.spreadsheets().batchUpdate(spreadsheetId=self.copyRange.sheetId, body=self.insert_request)
        print("request=", request)
        response = request.execute()
        print("response=", response)

@dataclass
class InsertRow:

    
    copyRange : CopyRange
    insert_request : {}
    
    def __init__(self, copyRange):
    
        self.copyRange = copyRange

        self.insert_request = {
            "requests": [
            {
                "insertDimension": {
                    "range": {
                    "sheetId": copyRange.sourceSheetId,
                    "dimension": "ROWS",
                    "startIndex": 0,
                    "endIndex": 1
                    },
                "inheritFromBefore": False
                },
            }
            ],
        }

    def insert_row ( self ) : 
    
        print("entered insert_row")
        request = self.copyRange.sheetservice.spreadsheets().batchUpdate(spreadsheetId=self.copyRange.sheetId, 
                                                                         body=self.insert_request)
        print("request=", request)
        response = request.execute()
        print("response=", response)



@dataclass
class SortCells:
    sort_request : {}
    sortRange   : CopyRange
    
    def __init__(self, sortRange):
    
        self.sortRange = sortRange
        self.sort_request =      {
                                "requests": [
                                    {
                                    "sortRange": {
                                        "range": {
                                            "sheetId": sortRange.targetSheetId,
                                            "startRowIndex": sortRange.startRowIndex,
                                            "endRowIndex": sortRange.endRowIndex,
                                            "startColumnIndex": sortRange.startColumnIndex,
                                            "endColumnIndex": sortRange.endColumnIndex
                                                },
                                    "sortSpecs": [
                                            {
                                            "dimensionIndex": 1,
                                            #"sortOrder": "ASCENDING"
                                            "sortOrder": "DESCENDING"

                                            },
                                            #{
                                            #"dimensionIndex": 3,
                                            #"sortOrder": "DESCENDING"
                                            #},
                                            #{
                                            #"dimensionIndex": 4,
                                            #"sortOrder": "DESCENDING"
                                            #}
                                                ]
                                            }
                                        }
                                    ]
                                }
        

    def sort_cells(self):
    
    
        request = self.sortRange.sheetservice.spreadsheets().batchUpdate(
                                                            spreadsheetId=self.sortRange.sheetId, 
                                                            body=self.sort_request)
                                                            
        print("request=", request)
        response = request.execute()
        print("response=", response)
        
        
        return


    
    