import json
from pathlib import Path

from .manager import UploadList, videoData
from .youtube import Youtube
from .auth import YoutubeAuth

from googleapiclient.discovery import MediaFileUpload

class YoutubeUpload(Youtube):
    def __init__(self):
        super().__init__()
        self.yt_auth = YoutubeAuth()
        self.upload_list_manager = UploadList()
        self.video_data_manager = videoData()

    def main(self, m_contents=None, m_contents_file=None):
        if m_contents:
            self.upload_list_manager.add_videos_to_upload_list(m_contents)
        
        if Path(str(m_contents_file)).is_file():
            f_m_contents_text = Path(str(m_contents_file)).read_text()
            f_m_contents = json.loads(f_m_contents_text)
            self.upload_list_manager.add_videos_to_upload_list(f_m_contents)
        
        m_contents = self.upload_list_manager.get_videos_to_upload()
        self.upload(m_contents)

    

    def upload(self, m_contents):
        for m_content in m_contents:
            if not m_content.get("video_filename"):
                continue
           
            music_file = Path(m_content.get("video_filename"))
         
            if not music_file.is_file() or not music_file.suffix in [".webm", ".mp4"]:
                continue
            yt_service = self.yt_auth.get_service()
            if not yt_service:
                continue
            
            try:
                data = self.video_data_manager.get_data(m_content)
                insert_request = yt_service.videos().insert(
                    part=",".join(data.keys()),
                    body=data,
                    media_body=MediaFileUpload(str(music_file))
                )

                response = insert_request.execute()
                print("youtube upload response: ",response)
            except:
                print("Error uploading to youtube", music_file, data)
                continue
            
            self.upload_list_manager.add_to_complete_list(m_content.get("post_id", str(music_file.absolute())), response)
            self.upload_list_manager.rm_video_from_upload_list(str(music_file.absolute()))
            self.yt_auth.update_app_upload_times()



if __name__ == "__main__":
    up = YoutubeUpload()
    m_contents = [{"tags":{"artist":"madoda", "title":"manager 2"},"post_id":2105, "permalink":"http://madodamusic.com/?p=5870", "video_filename":"vi.mp4", "youtube_z-index":22}]
    print("\n\n",up.main(m_contents))