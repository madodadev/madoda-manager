from pathlib import Path
import json
import os
from googleapiclient.discovery import build


from .accounts_manager import AccountsManager
# from folder_manager import FolderManagers
from .auth import Auth

class Gdive:
    def __init__(self):
        self.main_path = Path(__file__).parent.parent.parent.absolute()
        self.__main_conf_path = Path(str(self.main_path)) / str("assets/main_conf.json")
        self.__main_conf_key_name = "google_drive"
        self.__conf = {}
        self.__init_conf()



    
    def __init_conf(self):
        if self.__main_conf_path.exists():
            conf = json.loads( self.__main_conf_path.read_text() )
            self.__conf = conf[self.__main_conf_key_name]



    def __update_main_conf(self):
        if self.__main_conf_path.exists():
            conf = json.loads( self.__main_conf_path.read_text() )
  
            if conf.get("google_drive", 0):
                conf[self.__main_conf_key_name] = self.__conf
            else:
                conf.setdefault(self.__main_conf_key_name, self.conf)
          
            self.__main_conf_path.write_text(json.dumps(conf))
        
    
    
    def update_conf(self, key, value):
        if self.__conf.get(key, 0):
            self.__conf[key] = value
        else:
            self.__conf.setdefault(key, value)

        self.__update_main_conf()
    

    def get_gdrive_free_size(self, service):
        res = service.about().get(fields = "user, storageQuota").execute()
        free_space = int(res["storageQuota"]["limit"]) - int(res["storageQuota"]["usage"])

        return free_space
    

    def gdrive_have_space_to_upload_file(self, service, file, n_times=6):
        file_size = os.path.getsize(str(file))
        if ( file_size * n_times) < self.get_gdrive_free_size(service):
            return True
        else:
            return False



    
    
    

    @property
    def conf(self):
        return self.__conf

