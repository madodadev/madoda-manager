from uuid import uuid4
from pathlib import Path
import json
import os

def main():
    print("\n","=" * 20, "\tMADODA MANAGER GONF", "=" * 30,sep="\n", end="\n\n")
    gdrive = ConfigGdrive()
    gdrive_conf = gdrive.configAll()

    api_keys = ApiKeysConf()
    keys = api_keys.main()
    
    print("","="*10+"| google drive conf |"+"="*20,gdrive_conf, sep="\n", end="\n\n")
    print("","="*10+"| Auth conf |"+"="*20,keys, sep="\n", end="\n\n")
    os.environ["mm_main_path"] = str(Path(__file__).absolute())


class Setup():
    def __init__(self):
        self.main_path = Path(__file__).parent.absolute()
        self.main_conf_path = self.main_path / "assets/main_conf.json"

        if not self.main_conf_path.is_file():
            conf = {"global":{"main_path":str(self.main_conf_path)}}
            self.main_conf_path.write_text(json.dumps( conf ) )


class ConfigGdrive(Setup):
    def __init__(self):
        super().__init__()
        
        self.main_folder_id = None


    def get_main_folder_id(self):
        self.main_folder_id = input("insert google drive main folder id (root) \n\t=> ")
        if not self.main_folder_id: self.main_folder_id = "root"
        return self.main_folder_id


    def configAll(self):
        conf = json.loads( self.main_conf_path.read_text() )
        grive_conf = conf.get("google_drive", {})
        if conf:
            if not grive_conf.get("main_folder_id", 0):
                self.main_folder_id = self.get_main_folder_id()
            else:
                answer = input("main drive id allready exists do you want to chanhe(y/N): ")
                if str(answer) in ["y", "yes", "sim"]:
                    self.main_folder_id = self.get_main_folder_id()
            
            if self.main_folder_id:
                grive_conf["main_folder_id"] = self.main_folder_id
        else:
            grive_conf.setdefault("main_folder_id", self.get_main_folder_id())
        
        conf["google_drive"] = grive_conf
        self.main_conf_path.write_text(json.dumps(conf))
        return grive_conf


class ApiKeysConf(Setup):
    def __init__(self):
        super().__init__()
        self.conf = json.loads( self.main_conf_path.read_text() )
        if not self.conf.get("auth", 0):
            self.conf["auth"] = {}
        
        self.auth_conf = self.conf["auth"]
            
    
    def main(self):
        key = self.__generate_key()
        self.set_keys(key)
        api_keys = self.get_keys()
        self.conf["auth"] = self.auth_conf
        self.main_conf_path.write_text( json.dumps(self.conf) )
        return self.auth_conf

    
    def __generate_key(self):
        return uuid4()
    
    def get_keys(self):
        if self.auth_conf.get("api_keys", 0):
            return self.auth_conf.get("api_keys")
        return []
    
    def set_keys(self, key):
        api_keys = self.get_keys()
        if api_keys:
            r = input("there is at least one key, you want to add more? [y/N]: ")
            if r.lower() in ["y", "yes", "sim"]:
                api_keys.append(key)
        else:
            api_keys.append(str(key))
        
        self.auth_conf["api_keys"] = api_keys
    


if __name__ == "__main__":
    main()