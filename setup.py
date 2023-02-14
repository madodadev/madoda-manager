from uuid import uuid4
from pathlib import Path
import json
import os

from mm_uploads.youtube.auth import YoutubeAuth
def main():
    print("\n","=" * 20, "\tMADODA MANAGER GONF", "=" * 30,sep="\n", end="\n\n")
    gdrive = ConfigGdrive()
    gdrive_conf = gdrive.configAll()

    api_keys = ApiKeysConf()
    keys = api_keys.main()
    
    youtube_conf = YoutubeConf().main()

    print("","="*10+"| google drive conf |"+"="*20,gdrive_conf, sep="\n", end="\n\n")
    print("","="*10+"| Auth conf |"+"="*20,keys, sep="\n", end="\n\n")
    print("","="*10+"| Youtube Conf |"+"="*20,youtube_conf, sep="\n", end="\n\n")
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
        # api_keys = self.get_keys()
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
    


class YoutubeConf(Setup):
    def __init__(self):
        super().__init__()
        self.conf = json.loads( self.main_conf_path.read_text() )
        self.youtube_conf = self.conf.get("youtube", {})
        self.youtube_apps = self.youtube_conf.get("apps", {})
    
    def main(self):
        print("\n","=" * 20, "\tYoutube Gonf", "=" * 30,sep="\n", end="\n\n")
        self.get_apps_credentials()
        self.youtube_conf["apps"] = self.youtube_apps
        self.conf["youtube"] = self.youtube_conf
        self.main_conf_path.write_text( json.dumps(self.conf) )
        print("Do manuel make acess tokens run make_acess_token() in youtube.auth.py")
        resp = input("Do you want to make acess token NOW (Y/n): ")
        if resp.lower() not in ["n", "no"]:
            yt_auth = YoutubeAuth()
            yt_auth.make_acess_token()

        return self.youtube_conf

    
    def get_apps_credentials(self):
        while True:
            app_name = self.get_app_name()
            if app_name:
                oauth_client_id = self.get_oauth_client_id()
                if oauth_client_id:
                    client_ids_dir = Path(str(self.main_path)) / "assets/youtube/apps/{}/client_ids".format(app_name)
                    client_ids_dir.mkdir(parents = True, exist_ok=True)
                    oauth_client_id_file = client_ids_dir / "client_secret.json"
                    oauth_client_id_file.write_text(json.dumps(oauth_client_id))
                    self.youtube_apps[app_name]["OAuth_client_ID"] = str(oauth_client_id_file.absolute())
            
            res = input("Do you want to add another app (Y/n): ")
            if res in ["no", "n"]:
                return 1
            
    
    def get_app_name(self):
        app_name = input("Youtube App Name: ")
        if not app_name:
            return
            
        if not app_name in self.youtube_apps.keys():
            self.youtube_apps[app_name] = {}
            return app_name
        
        if not self.youtube_apps[app_name].get("OAuth_client_ID"):
            return app_name    
        
        res = input("App Name allreday have OAuth2.0 Client ID [DO YOU WANT TO CHANGE] (y/N)")
        if res.lower() in ["yes", "y"]:
            return app_name
        
        return False
    

    def get_oauth_client_id(self):
        while True:
            oauth_client_id_text =  input("Insert OAuth2.0 Client ID in JSON:\n")
            if oauth_client_id_text.lower() in ["x", "cancel"]:
                return False
            try:
                oauth_client_id = json.loads(oauth_client_id_text)
                return oauth_client_id
            except:
                print("Error check JSON Format or type X or cancel to cancel\n ")

                

            

if __name__ == "__main__":
    main()