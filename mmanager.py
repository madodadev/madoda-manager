import json
import threading
from pathlib import Path
from datetime import datetime

from mm_tags.edit import EditTags
from mm_downloads.download import Download
from mm_uploads.google_drive.upload import GdriveUpload

from mm_editor.audio_2_video import Audio2Video
from mm_uploads.youtube.upload import YoutubeUpload

class MMangaer:
    def __init__(self):
        self.dumps_folder = Path(__file__).parent / "dumps"
        self.m_contents = []
    
    def download_and_upload_to_gdrive(self, m_contents):
        m_contents = Download(m_contents).main()
        EditTags(m_contents).edit()
        m_contents = GdriveUpload(m_contents).mp3()
        m_contents_dump_file = self.dumps_folder / str(datetime.now().strftime("%Y_%m_%d.%H.%M.%S.json"))
        m_contents_dump_file.write_text(json.dumps(m_contents))
        self.m_contents = m_contents
        threading.Thread(target=self.task_make_video_and_upload_2_youtube).start()
        return m_contents, str(m_contents_dump_file.absolute())

    def task_make_video_and_upload_2_youtube(self, m_contents=None):
        if not m_contents: m_contents = self.m_contents
        m_contents = Audio2Video(m_contents).main()
        YoutubeUpload().main(m_contents)


if __name__ == "__main__":
    mm = MMangaer()
    m_contents = [{"filename":"music.mp3", "upload_to_youtube":1, "tags":{"artist":"mdd", "title":"manager 3"},"post_id":3421, "permalink":"http://madodamusic.com/?p=5870"}]
    mm.task_make_video_and_upload_2_youtube(m_contents)
