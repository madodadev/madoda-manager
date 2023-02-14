import os
from pathlib import Path
from googleapiclient.discovery import build

from .auth import Auth
class AccountsManager:
    def __init__(self):
        self.main_path = Path(__file__).parent.parent.parent.absolute()
        self.service_accounts_path = Path(os.path.join(str(self.main_path), "assets/google_drive/service_accounts"))
        self.client_ids_path = Path(os.path.join(str(self.main_path), "assets/google_drive/client_ids"))
        self.full_accounts_path = Path(os.path.join(str(self.main_path), "assets/google_drive/full_accounts.txt"))
        self.__is_service_account = False
    
    def getFullAccount(self):
        if self.full_accounts_path.exists():
            full_accounts = full_accounts_path.read_text().split("\n")
            return full_accounts
        
        return []
            
        

    def setFullAccount(self, account):
        self.full_accounts_path.write_text(str(account)+"\n")

    
    def __get_folder_size(self,folder):
        music_path = Path(folder)
        size = 0
        for music in music_path.iterdir():
            if str(music).endswith(".mp3"):
                size += int(os.path.getsize(str(music)))
        
        return size
    
    
    
    def __get_file_size(self, file):
        return os.path.getsize(str(file))
    
    
    
    def __get_gdrive_free_size(self, account, is_service_account=None):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        auth = Auth(SCOPES, account)
        creds = auth.getCreds()

        service = build('drive', 'v3', credentials=creds)
        res = service.about().get(fields = "user, storageQuota").execute()
        free_space = int(res["storageQuota"]["limit"]) - int(res["storageQuota"]["usage"])

        return free_space


    def getCredFile(self, not_those=[]):
        full_accounts = self.getFullAccount()
        if self.client_ids_path.exists():
            for ac in self.client_ids_path.iterdir():
                if str(ac) not in full_accounts and str(ac.suffix) == ".json":
                    if str(ac) not in not_those:
                        return str( ac.absolute() )
                    else:
                        print("less space in: "+str(ac))
                else:
                    print(str(ac)+" [IS FULL]")
        

        if self.service_accounts_path.exists():
            for ac in self.service_accounts_path.iterdir():
                if str(ac) not in full_accounts and str(ac.suffix) == ".json":
                    if str(ac) not in not_those:
                        return str( ac.absolute() )
                    else:
                        print("less space in: "+str(ac))
                else:
                    print(str(ac)+" [IS FULL]")
        
        return False

    
    def getIsServiceAccount(self):
        return self.__is_service_account
    
    
    def update_account(self, account):
        if self.__get_gdrive_free_size(account) < 100000000:
            self.setFullAccount(account)
    


if __name__ == "__main__":
    am = AccountsManager()
    # am.update_account(am.getCred("/mnt/x/workspace/madoda-manager/musics/"))
    am.getCred("X:\\workspace\\madoda-manager\\musics")
    # am.update_account()
