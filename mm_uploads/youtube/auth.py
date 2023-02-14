import pickle
import random
from pathlib import Path
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
if __name__ == "__main__":
    from youtube import Youtube
else:
    from .youtube import Youtube


class YoutubeAuth(Youtube):
    def __init__(self):
        super().__init__()
        self.scope = ["https://www.googleapis.com/auth/youtube"]
        self.youtube_apps = self.conf.get("apps", {})
        self.yt_app_max_upload_per_day = 5
        self.today = str(datetime.today().strftime("%d/%m/%Y"))
        self.yt_channel = None
        self.current_app = None
    
    
    def get_service(self, channel=None):
        self.yt_channel = channel
        for n in range(10):
            token_file =  self.get_acess_token()
            try:
                if token_file and Path(str(token_file)).is_file():
                    token_file = Path(str(token_file))
                    creds = pickle.loads(token_file.read_bytes())
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    service = build("youtube", "v3", credentials = creds)
                    return service        
            except:
                print(n, "Error Get Acess Token", token_file)
        return False
        

    
    def get_acess_token(self):
        for app, content in self.youtube_apps.items():
            if not content.get("last_use"):
                self.youtube_apps[app]["last_use"] = {"date": self.today, "upload_times":0 }
                self.update_conf("apps", self.youtube_apps)
                self.current_app = app
                return self.get_token_from_app(app)

            if not content["last_use"].get("date") == self.today:
                self.youtube_apps[app]["last_use"] = {"date": self.today, "upload_times":0 }
                self.update_conf("apps", self.youtube_apps)
                self.current_app = app
                return self.get_token_from_app(app)
            
            if int(content["last_use"].get("upload_times")) <= self.yt_app_max_upload_per_day:
                self.current_app = app
                return self.get_token_from_app(app)
        
    
    def get_token_from_app(self, app):
        yt_cannels = self.youtube_apps[app]["channels"]
        if self.yt_channel:
            if self.yt_channel in yt_cannels.keys():
                token_file_path =  yt_cannels[self.yt_channel].get("token_file_path")
                if Path(str(token_file_path)).is_file():
                    return token_file_path
        else:
            yt_cannels = {k:v for (k, v) in yt_cannels.items() if int(v.get("upload_random_videos", 0)) == 1}
            while yt_cannels:
                channel = random.choice(list(yt_cannels.keys()))
                token_file_path =  yt_cannels[channel].get("token_file_path", "")
                if Path(str(token_file_path)).is_file():
                    return token_file_path
                
                yt_cannels.pop(channel)
            
        
        return False

    
    def update_app_upload_times(self):
        self.youtube_apps[self.current_app]["last_use"]["date"] = self.today
        self.youtube_apps[self.current_app]["last_use"]["upload_times"] +=  1
        self.update_conf("apps", self.youtube_apps)
    
    def make_acess_token(self):
        channels_mun = int(input("how many channels for each app: "))
        for index, conetnt in self.youtube_apps.items():
            if conetnt.get("OAuth_client_ID"):
                youtube_channels = conetnt.get("channels", {})
                for num in range(channels_mun):
                    channel_name = input("The {}o Channel Name you want to connect with {}: ".format(num + 1, index))
                    if channel_name not in youtube_channels.keys():youtube_channels[channel_name] = {}
                    client_secrets_file = conetnt.get("OAuth_client_ID")
                    flow = InstalledAppFlow.from_client_secrets_file(
                            client_secrets_file, self.scope)
        
                    creds = flow.run_console()
                    tokens_dir = self.main_youtube_path / "apps" / str(index) / "tokens"
                    tokens_dir.mkdir(parents = True, exist_ok = True)
                    token_file_path = tokens_dir / str(channel_name+"_token.pickle")
                    with open( token_file_path, 'wb') as token:
                        pickle.dump(creds, token)
                    
                    youtube_channels[channel_name]["token_file_path"] = str(token_file_path.absolute())

                    res = input("upload random videos de this channel (Y/n)")
                    if res in ["no", "n"]:
                        youtube_channels[channel_name]["upload_random_videos"] = 0
                    else:
                        youtube_channels[channel_name]["upload_random_videos"] = 1


                conetnt["channels"] = youtube_channels  
                self.youtube_apps[index] = conetnt
                self.update_conf("apps", self.youtube_apps)



if __name__ == "__main__":
    auth = YoutubeAuth()
    # auth.make_acess_token()
    youtube = auth.get_service()
    request = youtube.channels().list(
        part="statistics",
        id="UCC1JYsEKLRO5i3J-LhQOvSg"
    )
    response = request.execute()

    print(response)

    



