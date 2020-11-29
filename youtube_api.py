import pickle
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from googleapiclient.discovery import MediaFileUpload
def auth():
    #desktop Client
    CLIENT_SECRETS_FILE = "___mm_ysf.json"
    YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    creds = None
    token_path = "token.pickle"
    token_file = Path(str(token_path))
    if token_file.is_file():
        creds = pickle.loads(token_file.read_bytes())
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                            CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
            
            creds = flow.run_console()

    with open( token_path, 'wb') as token:
        pickle.dump(creds, token)

    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials = creds)
    return service

youtube = auth()
# request = youtube.channels().list(
#     part="statistics",
#     id="UCC1JYsEKLRO5i3J-LhQOvSg"
# )
# response = request.execute()

# print(response)
data = {
    "snippet" : {
        "title": "new v3 04",
        "description": "madoda youtube upload",
        "tags": ["madoda", "2020"],
        "categoryId": "20"
    },
    "status": {
        "privacyStatus":"public",
        "selfDeclaredMadeForKids": "false"
    }
}

music_file = Path("vi.mp4")
insert_request = youtube.videos().insert(
    part=",".join(data.keys()),
    body=data,
    media_body=MediaFileUpload(str(music_file))
)

response = insert_request.execute()

print(response)