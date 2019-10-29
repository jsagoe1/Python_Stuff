from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload,MediaIoBaseDownload

import auth
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
SECRET_FILE = r"credentials.json"   ## this file needs to be in current working directory
APPLICATION_NAME = "Drive API Python Quickstart"

authInstance = auth.auth(SCOPES, SECRET_FILE, APPLICATION_NAME)
credentials = authInstance.getCredentials()

drive_service = build('drive', 'v3', credentials=credentials)

class gDrive:
    """
    Class for performing googledrive operations
     - All querries do no include "Shared With Me" and "Bin" folder
    """
    
    def listAllItems(self, num=1000, itemType='all'):
        """
        Lists all items in Drive.
         - can select between files, folders or all
        
        Returns a dictionary:
            key: item_name
            value: item_ID
        """
        try:
            if itemType == 'all':
                elements = drive_service.files().list(pageSize=num, q="'me' in owners").execute()
            elif itemType == 'files':
                elements = drive_service.files().list(pageSize=num,
                                                      q=r"mimeType!='application/vnd.google-apps.folder' and 'me' in owners and trashed=false").execute()
                                                      
            elif itemType == 'folders':
                elements = drive_service.files().list(pageSize=num, 
                                               q=r"mimeType='application/vnd.google-apps.folder' and 'me' in owners and trashed=false").execute()
                                               
            items = elements.get('files', [])
            
            if not items:
                return None
            else:
                item_list = {}
                for item in items:
                    item_list[u'{}'.format(item['name'])] = [u'{}'.format(item['id'])]
                return item_list
        
        except:
            print("ParameterError: Please Check the parameters\n")
            
            
    def listItemsinFolder(self, folderName='root', num=1000, itemType='all'):
        """
        list items in a particular folder.
        created this because I need the folder ID before hand so I had to
        create another function to show all items in drive so I can use that 
        to retrieve the folder ID
        """
        if folderName == 'root':
            return self.listAllItems(num, itemType)
        
        else:
            if not self.isExist(folderName): #if folder does not exist
                print("Folder does not exist")
                return None
                
            else:
                folderID = self.__find_folderID(folderName)   #get folder ID
                if itemType == 'folders':
                    return self.listDirectorySubFolders(folderName)
                    
                elif itemType == 'files' or itemType=='all':
                    if itemType == 'files':
                        elements = drive_service.files().list(q = r"mimeType!='application/vnd.google-apps.folder' and '{}' in parents and 'me' in owners and trashed=false".format(folderID)).execute()
                    elif itemType == 'all':
                        elements = drive_service.files().list(q = r"'{}' in parents and 'me' in owners and trashed=false".format(folderID)).execute()
                    
                    items = elements.get('files', [])
                    if not items:
                        print("\'{}\' does not contain specified itemtype".format(folderName))
                        return None
                    else:
                        item_list = {}
                        for item in items:
                            item_list[u'{}'.format(item['name'])] = [u'{}'.format(item['id'])]
                        return item_list
                
                else:
                    print("itemType is invalid. Accepts only 'files' or 'folders'")    
                    return None

    def __find_folderID(self, folderName):
        """
        To find the ID of a folder
        return: Folder_ID
        """
        name_id = self.listAllItems(itemType='folders')
        return name_id[folderName][0]
        

    def listRootDirectoryFolders(self):
        """
        Lists the folders in the root directory
        return:
            dictionary:
                key: folder name
                value: folder ID
        """
        folders = drive_service.files().list(q = r"mimeType='application/vnd.google-apps.folder' and 'root' in parents and 'me' in owners and trashed=false").execute()
        items = folders.get('files', [])
        if not items:
            return None
        else:
            folder_list = {}
            for item in items:
                folder_list[u'{}'.format(item['name'])] = [u'{}'.format(item['id'])]
            return folder_list    
            

    def listDirectorySubFolders(self, folderName):
        """
        Lists all the sub-directories  in folderName
        return:
            dictionary:
                key:sub folder name
                value: sub folder ID
        """
        if folderName == "root":              # this is really not neccessary
            return self.listRootFolders()
        else:
            try:
                folderID = self.__find_folderID(folderName)
                folders = drive_service.files().list(q = r"mimeType='application/vnd.google-apps.folder' and '{}' in parents and 'me' in owners and trashed=false".format(folderID)).execute()
                items = folders.get('files', [])
                if not items:
                    print("\'{}\' contains no sub-folders".format(folderName))
                    return None
                else:
                    folder_list = {}
                    for item in items:
                        folder_list[u'{}'.format(item['name'])] = [u'{}'.format(item['id'])]
                    return folder_list
                
            except:
                print("Folder does not exist")
                
        
    def isExist(self, fileOrFolderName, location='root'):
        """
        check whether file or folder exists in a location
        """
        
        x = self.listAllItems()             # get list of all items
        if location != 'root':
            if location in x.keys():        # check if location exists
                y = self.listItemsinFolder(location)
                if fileOrFolderName in y.keys():
                    return True
                else:
                    return False 
        else:
            if fileOrFolderName in x.keys():
                return True
            return False
        
    
    def createFolder(self, folderName, destination=None):
        """
        create a folder in location
        default location:root directory
        return newfolderID
        """
        
        if destination == None:                                 # if destination is not specified
            destination  = 'root'
            destinationID = 'root'
            if self.isExist(folderName, 'root'):
                print("\'{}\' already exists in root folder".format(folderName))
                return None
            else:
                return self.__create(folderName=folderName, type='folder', destinationID='root')                
        
        else:                                                   # if destination parameter is specified
            if self.isExist(destination):                       # check if destination exists
                if self.isExist(folderName, destination):       #check if folder already exists in destination
                    print("There is a folder already named \'{}\' in the specified location".format(folderName))
                    return None
                else:                                           # if folder does not exist, create the folder in destination
                    destinationID = self.__find_folderID(destination)    # get the destination ID
                    return self.__create(folderName=folderName, type='folder', destinationID=destinationID)
            else:
                print("The specified destination does not exist on Drive")
                return None
                
    
    def uploadFile(self, fileName, filePath, destination=None):
        """
        upload a file or folder 
        return ID of uploaded file
        """
        if destination == None:                                 # if destination is not specified
            destination  = 'root'
            destinationID = 'root'
            if self.isExist(fileName, 'root'):
                print("\'{}\' already exists in root folder".format(fileName))
                return None
            else:
                return self.__upload(fileName=fileName, filePath=filePath, destinationID='root')                
        
        else:                                                   # if destination parameter is specified
            if self.isExist(destination):                       # check if destination exists
                print("destination found")
                if self.isExist(fileName, destination):         #check if folder already exists in destination
                    print("There is a file already named \'{}\' in the specified location".format(fileName))
                    return None
                else:                                           # if folder does not exist, create the folder in destination
                    destinationID = self.__find_folderID(destination)    # get the destination ID
                    return self.__upload(fileName=fileName, filePath=filePath, destinationID=destinationID)
            else:
                print("The specified destination does not exist on Drive")
                return None        

    
    def __upload(self, fileName, filePath, destinationID):
        """
        upload a file to destinationID
        """
        
        body = {'name': fileName,
                'mimeType': '*/*',
                'parents': destinationID} 
                
        media = MediaFileUpload(filePath,
                                mimetype='*/*',
                                resumable=True)
                                
        uploadedFile = drive_service.files().create(body=body, media_body=media).execute()
        print("Uploaded \'{}\' in specified destination. ID of new file: \'{}\'".format(filePath, uploadedFile['id']))
        return uploadedFile['id']
        
        
                
    def __create(self,fileORFolderName=None, type=None, destinationID=None):
        """
        create a file or folder in destinationID
        Returns: ID of created file or folder
        """
        if type == 'folder':
            mimeType = "application/vnd.google-apps.folder"
        elif type == 'file':
            mimeType = "application/vnd.google-apps.file"
        
        body = {'name': fileORFolderName,
                'mimeType': mimeType,
                'parents': destinationID}
                    
        created_folder = drive_service.files().create(body = body).execute()
        print("Created \'{}\' in specified destination. ID of new folder: \'{}\'".format(fileORFolderName, created_folder['id']))
        return created_folder['id']
        
        
        
    
    
##test instance       
drive = gDrive()
