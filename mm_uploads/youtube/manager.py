import json
from pathlib import Path

from .youtube import Youtube

class UploadList(Youtube):
    def __init__(self):
        super().__init__()
        self.__videos_to_upload_file = Path(str(self.main_youtube_path)) / str("videos_to_upload.json")
        self.__videos_to_upload = self.get_videos_to_upload()
    
   
    def __sorte_videos_to_upload(self, m_content):
        z_index = m_content.get("youtube_z-index", 0)
        return z_index
    


    def is_file_in_upload_list(self, filename):
        videos_to_upload = self.get_videos_to_upload()
        for video_to_upload in videos_to_upload:
            if str( video_to_upload.get("video_filename", "") ) == str(filename):
                return True
        return False



    def get_videos_to_upload(self):
        if self.__videos_to_upload_file.is_file():
            videos_to_upload_text = self.__videos_to_upload_file.read_text()
            videos_to_upload = json.loads(videos_to_upload_text)
            videos_to_upload.sort(key=self.__sorte_videos_to_upload, reverse=True)
            return videos_to_upload
        else:
            self.__videos_to_upload_file.write_text(json.dumps([]))
            return []

    
    def add_videos_to_upload_list(self, m_contents):
        for m_content in m_contents:
            video_path = m_content.get("video_filename", "")
            if self.is_file_in_upload_list(video_path):
                self.rm_video_from_upload_list(video_path)
            self.__videos_to_upload.append(m_content)
        self.__videos_to_upload_file.write_text(json.dumps(self.__videos_to_upload))


    def rm_video_from_upload_list(self, video_path):
        for index, video in enumerate(self.__videos_to_upload):
            if str( video.get("video_filename", "") ) == str(video_path):
                self.__videos_to_upload.pop(index)
        self.__videos_to_upload_file.write_text(json.dumps(self.__videos_to_upload))


if __name__ == "__main__":
    upl = UploadList()
    upl.add_videos_to_upload_list([{"title":"KB", "video_filename": "KDrive.mp4", "youtube_z-index":5}])
    # upl.rm_video_from_upload_list("Drive.mp4")
    res = upl.get_videos_to_upload()
    print(res)