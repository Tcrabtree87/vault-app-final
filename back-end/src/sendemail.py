from __future__ import print_function

import os
import mimetypes
import base64
from email.message import EmailMessage


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


    
def gmail_send_message(creds, subject, filename, recipient):
    
    try:
    
        service = build('gmail', 'v1', credentials=creds)
        
        message = EmailMessage()

        message.set_content('Your counts report is ready')

        message['From'] = 'jeffrey.goodwin@lacity.org'
        message['To'] = recipient
        message['Subject'] = subject

        
        # pylint: disable=E1101
        
        # attachment
        #filename = 'ui-test-matter-001-query-api.csv'
        attachment_filename = 'log-files' + '\\' + filename
        # current directory
        curdir = os.getcwd()
        print("curdir=",curdir)
        
        # guessing the MIME type
        type_subtype = mimetypes.guess_type(attachment_filename)
        
        print("type_subtype=", type_subtype)
        
        if(type_subtype == False):
            print("unrecognized file type")
        else:
            #maintype, subtype = type_subtype
            maintype = type_subtype[0]
            subtype = "octet-stream"

            with open(attachment_filename, 'rb') as fp:
                attachment_data = fp.read()
                
            #print("attachment_data=", attachment_data)

            message.add_attachment(attachment_data, maintype=maintype, subtype=subtype, filename=filename)
            
            
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            create_message = {
            'raw': encoded_message
            }
            
    
            # comment out sending the email
            
            #send_message = create_message
            send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
            
            
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message
