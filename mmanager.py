import json
from pathlib import Path
from datetime import datetime

from mm_tags.edit import EditTags
from mm_downloads.download import Download
from mm_uploads.google_drive.upload import GdriveUpload
class MMangaer:
    def __init__(self):
        self.dumps_folder = Path(__file__).parent / "dumps"
    
    def download_and_upload_to_gdrive(self, m_contents):
        m_contents = Download(m_contents).main()
        EditTags(m_contents).edit()
        m_contents = GdriveUpload(m_contents).mp3()
        m_contents_dump_file = self.dumps_folder / str(datetime.now().strftime("%Y_%m_%d.%H.%M.%S.json"))
        m_contents_dump_file.write_text(json.dumps(m_contents))
        return m_contents, str(m_contents_dump_file.absolute())


if __name__ == "__main__":
    mm = MMangaer()
    m_contents = [{"download_url":"https://www.youtube.com/watch?v=z29nI8RQV0U","gdrive_upload_times":5, "post_id":22, "tags":{"artist": "Chris Brown", "title":"Don't Judge Me"} }]
    print(mm.download_and_upload_to_gdrive())
