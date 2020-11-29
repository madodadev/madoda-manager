import pickle
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .youtube import Youtube


class Auth(Youtube):
    def __init__(self):
        super().__init__()
        self.client_secrets_file = "___mm_ysf.json"
        self.scope = "https://www.googleapis.com/auth/youtube"
    
    def __make_acess_token(self):
        channels_mun = input("how many channels for each app: ")
        
    



