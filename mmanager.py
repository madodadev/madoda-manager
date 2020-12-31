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
    
    def main(self, m_contents):
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
    m_contents = [{"post_id":"6636","download_url":"https://docs.google.com/uc?export=download&id=19z_daIlcKuDoSHjn3ZRiTzDaD-dbdg2x","permalink":"http://madodamusic.com/baixar-musica-de-mr-bow-only-you/","gdrive_upload_times":6,"tags":{"artist":"Mr bow","title":"Only You"},"youtube_z-index":0,"upload_to_gdrive":0,"upload_to_youtube":1,"save_as":"Mr bow - Only You", "filename":"music.mp3"}]
    mm.main(m_contents)
