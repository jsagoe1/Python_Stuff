To use this GoogleDrive project:

  you will need the following:
    - install google drive API for python
    - secret .json credential file from google
    - place that credential file in your current working directory


Help on gDrive in module __main__ object:

class gDrive(builtins.object)
 |  Class for performing googledrive operations
 |   - All querries do no include "Shared With Me" and "Bin" folder
 |  
 |  Methods defined here:
 |  
 |  createFolder(self, folderName, destination=None)
 |      create a folder in location
 |      default location:root directory
 |      return newfolderID
 |  
 |  isExist(self, fileOrFolderName, location='root')
 |      check whether file or folder exists in a location
 |  
 |  listAllItems(self, num=1000, itemType='all')
 |      Lists all items in Drive.
 |       - can select between files, folders or all
 |      
 |      Returns a dictionary:
 |          key: item_name
 |          value: item_ID
 |  
 |  listDirectorySubFolders(self, folderName)
 |      Lists all the sub-directories  in folderName
 |      return:
 |          dictionary:
 |              key:sub folder name
 |              value: sub folder ID
 |  
 |  listItemsinFolder(self, folderName='root', num=1000, itemType='all')
 |      list items in a particular folder.
 |      created this because I need the folder ID before hand so I had to
 |      create another function to show all items in drive so I can use that 
 |      to retrieve the folder ID
 |  
 |  listRootDirectoryFolders(self)
 |      Lists the folders in the root directory
 |      return:
 |          dictionary:
 |              key: folder name
 |              value: folder ID
 |  
 |  uploadFile(self, fileName, filePath, destination=None)
 |      upload a file or folder 
 |      return ID of uploaded file
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
