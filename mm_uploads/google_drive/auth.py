from __future__ import print_function
import pickle
import os.path
import json
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class Auth:
    def __init__(self, SCOPES, credential):
        self.SCOPES = SCOPES
        self.credential = Path(str(credential))
        self.creds = None
        self.is_service_account = False
        
        if self.credential.exists():
            try:
                credfile = self.credential.read_text()
                if credfile.find("service_account"):
                    self.is_service_account = True    
            except:
                print("error checking that {} is service account or not".format(self.credential))
 
        
    
    def __auth_by_service_account(self):
        self.creds = service_account.Credentials.from_service_account_file(self.credential, scopes=self.SCOPES)
    
    
    
    def __auth_by_client_id_OAuth(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)   
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credential, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    
    
    
    def __auth(self):
        if self.credential.exists():
            try:
                if( self.is_service_account ):
                    self.__auth_by_service_account()
                else:
                    self.__auth_by_client_id_OAuth()
            except:
                print("ERROR AUTH WITH ", self.credential)
        else:
            print("NO CREADTIONAL [PLASE ADD ONE]")
            
    def getCreds(self):
        self.__auth()
        return self.creds


if __name__ == "__main__":
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # credf = Path("X:\\workspace\\madoda-manager\\assets\\google_drive\\service_accounts\\manager-284002-59aaad1f2be2.json")
    credf = Path("/mnt/x/workspace/madoda-manager/assets/google_drive/service_accounts/manager-284002-59aaad1f2be2.json")
    auth = Auth(SCOPES, credf)
    # auth.is_service_account = True
    print(credf.exists())
    print("is service account", auth.is_service_account)
    print("cred", auth.getCreds())


