from __future__ import print_function
import datetime
import os
from pathlib import Path
from .gdrive import Gdive
from .auth import Auth
from .accounts_manager import AccountsManager
from googleapiclient.discovery import build

class FolderManager(Gdive):
    def __init__(self, gdrive_service):
        super().__init__()
        self.service = gdrive_service
        if self.conf.get("main_folder_id", 0):
            self.main_drive_folder_id = self.conf["main_folder_id"]
        else:
            self.main_drive_folder_id = "root"
        
        self._content_folder_id = 0
        self._gdrive_path_folders_ids = []
        self.__drive_log_folder_name = "logs"
        self.__log_folder_id = 0
        self.__base_log_folder_id = 0
        

    
    def _ceackFolder(self, folder_name, parent_folder_id):
        page_token = None
        while True:
            response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, parents)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                if file.get('name') == folder_name:
                    try:
                       if file.get('parents')[0] == parent_folder_id:
                            return file.get('id')
                    except:
                        pass
                    
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return False
    
    
    def createNewFolder(self, folder_name, parent_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            "parents": [parent_id]
        }
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
    
        return file.get('id')


            
    def create(self, folders):
        base_parent_folder_id, base_folder_id = self.create_gdrive_folder_from_date_Y_M(self.main_drive_folder_id)
        parent_id = base_folder_id
        for index, folder in enumerate(folders):                           
            content_folder_id = self._ceackFolder(folder, parent_id)
            if not content_folder_id:
                content_folder_id = self.createNewFolder(folder, parent_id)
            
            parent_id = content_folder_id

            self._gdrive_path_folders_ids.append(content_folder_id)
            self._content_folder_id = content_folder_id
        
        self._create_gdrive_log_folder_id()
            
        return content_folder_id
    
    
    
    def create_gdrive_folder_from_date_Y_M(self, main_parent_id=None):
        year_folder_name = str(datetime.datetime.today().year)
        month_folder_name = str(datetime.datetime.today().month)
        if not main_parent_id: main_parent_id = self.main_drive_folder_id
        year_folder_id = self._ceackFolder(year_folder_name, main_parent_id)
        if year_folder_id:
            month_folder_id = self._ceackFolder(month_folder_name, year_folder_id)
            if not month_folder_id:
                month_folder_id = self.createNewFolder(month_folder_name, year_folder_id)        
        else:
            year_folder_id = self.createNewFolder(year_folder_name, main_parent_id)
            month_folder_id = self.createNewFolder(month_folder_name, year_folder_id)
        
        return year_folder_id, month_folder_id


    
    def _create_gdrive_log_folder_id(self):
        self.__base_log_folder_id  = self._ceackFolder(self.__drive_log_folder_name, self.main_drive_folder_id)
        if not self.__base_log_folder_id:
            self.__base_log_folder_id = self.createNewFolder(self.__drive_log_folder_name, self.main_drive_folder_id)
        
        parent_folder_id, content_folder_id = self.create_gdrive_folder_from_date_Y_M(self.__base_log_folder_id)
        self.__log_folder_id = content_folder_id
        return content_folder_id

    @property
    def content_folder_id(self):
        return self._content_folder_id
    
    @property
    def gdrive_path_folders_ids(self):
        return self._gdrive_path_folders_ids
    
    @property
    def log_folder_id(self):
        return self.__log_folder_id
    
    @property
    def base_log_folder_id(self):
        return self.__base_log_folder_id
        





class ServiceManager(Gdive):
    def __init__(self):
        super().__init__()
        self.__accounts_manager = AccountsManager()
        self.__credential_file = self.__accounts_manager.getCredFile()
        self.SCOPES = ['https://www.googleapis.com/auth/drive']


    def build_gdrive_service(self, SCOPES):
        self.SCOPES = SCOPES
        self.auth = Auth(SCOPES, self.__credential_file)
        self.creds = self.auth.getCreds()

        self.service = build('drive', 'v3', credentials=self.creds)
        return self.service



    def build_new_gdrive_service(self, filename,  gdrive_upload_times):
        credential_file_with_no_space = [self.__credential_file]
        while True:
            self.__credential_file = self.__accounts_manager.getCredFile(credential_file_with_no_space)
            if not self.__credential_file:
                return False

            creds = Auth(self.SCOPES, self.__credential_file).getCreds()
            self.service = build('drive', 'v3', credentials=creds)
          
            if self.gdrive_have_space_to_upload_file(self.service, filename, gdrive_upload_times):
                return self.service
            else:
                credential_file_with_no_space.append(self.__credential_file)

    @property
    def credential_file(self):
        return self.__credential_file
        

if __name__ == "__main__":
        am = AccountsManager()
        account = am.getCred(__file__)
        SCOPES = ['https://www.googleapis.com/auth/drive']
        auth = Auth(SCOPES, account)
        creds = auth.getCreds()
        service = build('drive', 'v3', credentials=creds)
        fm = FolderManager(service)
        fm.create(("madoda", "manager"))

        print("base log folder id: ",fm.base_log_folder_id)
        print("log folder id: ",fm.log_folder_id)
        print("content folder id: ",fm.content_folder_id)
