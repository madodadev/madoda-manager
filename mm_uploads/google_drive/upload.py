from __future__ import print_function
import pickle
import os.path
from pathlib import Path
import os
import datetime
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

from .auth import Auth
from .gdrive_manager import FolderManager, ServiceManager
from .accounts_manager import AccountsManager
from .gdrive import Gdive

class GdriveUpload(Gdive):
    def __init__(self, m_contents):
        super().__init__()
        self.m_contents = m_contents
        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.sm = ServiceManager()
        self.service = self.sm.build_gdrive_service(SCOPES)
       
        self.copy_folders_ids = []
        self.new_files_id = {}


    def __upload_mp3_multi_temes(self, file_name, parent_id="root", n=6):
        gdrive_ids = []
        if str(file_name).endswith(".mp3"):
            for num in range(n):
                file_metadata = {
                    'name': str(file_name.name), 
                    "parents": [parent_id]
                }
                media = MediaFileUpload(str(file_name), mimetype='audio/mp3')
                Dfile = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                gdrive_ids.append(Dfile.get('id'))

            # self.new_files_id.setdefault(str(file_name), gdrive_ids)

            return gdrive_ids
        else:
            return "error: not a mp3 file"

    
    def _upload_file(self, file, parent_id, mimetype= "text/plain"):
        file_metadata = {
            'name': os.path.basename(file), 
            "parents": [parent_id]
        }
        media = MediaFileUpload(file, mimetype=mimetype)
        Dfile = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return Dfile.get('id')


    def _create_file_with_all_ids(self, new_files_id):
        log_folder_path = os.path.join(str(self.main_path), "assets/gdrive_log")
        if self.gdrive_folder_base_name:
            log_name = str(self.gdrive_folder_base_name)
        else:
            log_name = str(datetime.datetime.today())
        
        log_file_text = os.path.join(log_folder_path, log_name+".txt")
        log_file_json = os.path.join(log_folder_path, log_name+".json")
        
        #create file with all drive urls to use with madoda_getway
        drive_urls = open("drive_urls.json", "w")
        drive_urls.write(json.dumps(new_files_id))
        drive_urls.close()
        
        #make file that is suported by madoda-music theme
        mdd_new_file_ids = str(new_files_id).replace("',", "&&\n")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("'", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace(":", ":\n")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("],", "\n\n\n")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("{", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("[", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("]", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("}", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace(" ", "")
        
        if os.path.exists(log_folder_path):
            log_txt = open(log_file_text, "w")
            log_json = open(log_file_json, "w")
            
            log_txt.write(str(mdd_new_file_ids))
            log_json.write(json.dumps(new_files_id))
        else:
            os.makedirs(log_folder_path)
            log_txt = open(log_file_text, "w")
            log_json = open(log_file_json, "w")
            
            log_txt.write(str(mdd_new_file_ids))
            log_json.write(json.dumps(new_files_id))
        
        log_txt.close()
        log_json.close()
        return [log_file_text, log_file_json]
    
    def get_folders_name_by_m_content_tags(self, m_content_tags):
        if (m_content_tags.get("artist", 0) and m_content_tags.get("title", 0)):
            main_folder = m_content_tags.get("artist")
            sec_folder = m_content_tags.get("title")
            return (main_folder, sec_folder)
        
        return False
        


    def mp3(self):
        for index, content in enumerate(self.m_contents):
            filename = Path(content.get("filename", 0))
            if Path(filename).exists() and filename:
                gdrive_upload_times = int(content.get("gdrive_upload_times", 6))
                if not self.gdrive_have_space_to_upload_file(self.service, filename, gdrive_upload_times):
                   if not self.sm.build_new_gdrive_service(filename, gdrive_upload_times):
                       continue
                folders = self.get_folders_name_by_m_content_tags(content.get("tags", {}))
                if not folders: folders = ("unknown", filename.stem)
                gdrive_folder_id = FolderManager(self.service).create(folders)
                gdrive_ids = self.__upload_mp3_multi_temes(filename, gdrive_folder_id, gdrive_upload_times)
                self.m_contents[index]["gdrive_ids"] =  gdrive_ids
        
        return self.m_contents
               
    
        
if __name__ == "__main__":
    up = GdriveUpload()