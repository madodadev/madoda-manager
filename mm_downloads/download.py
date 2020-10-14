from pathlib import Path
from datetime import datetime
import os.path
import urllib.request

from youtube import YoutubeDownload
class Download:
    def __init__(self, m_content):
        self.m_contents = m_content
        
        self.musics_base_folder = Path(__file__).absolute().parent.parent / Path("musics") 
        if not self.musics_base_folder.exists():
            self.musics_base_folder.mkdir()
        
        self.save_folder = self.musics_base_folder / str(datetime.now().strftime("%Y_%m_%d.%H.%M.%S"))
        if not Path(str(self.save_folder)).exists():
            Path(str(self.save_folder)).mkdir()



    def getUrlType(self, url):
        url = str(url).lower().replace(" ", "")
        sites = {"youtube":"https://www.youtube.com/", "gdrive":"https://docs.google.com/uc?export=download&id="}
        for index, site in sites.items():
            if url.startswith(site.lower()):
                return index
            
            if url.endswith(".mp3"):
                return "direct_url"
        
        return False

    
    
    def isFileExsite(self, filename):
        if filename:
            if Path(str(filename).lstrip()).exists():
                return True
        return False
    
    
    def getNameByTags(self, tags):
        if tags.get("artist") and tags.get("title"):
            return tags.get("artist") +" - "+ tags.get("title")
        return False


    def getOutputName(self, content):
        filename = content.get("save_file_as")
        tags = content.get("tags")
        if filename:
            return Path(str(filename))
        elif tags:
            name = self.getNameByTags(tags)
            if name:
                return Path(str(name))
        
        return False


    def youtubeDl(self, m_content):
        index, content = m_content
        download_url = content.get("download_url")
        yt_download = YoutubeDownload(self.save_folder)
        output_name = self.getOutputName(content)
        filename = yt_download.mp3(download_url, output_name)
        self.m_contents[index]["filename"] = str(filename)



    def direct_urlDl(self, m_content):
        index, content = m_content
        download_url = content.get("download_url")
        output_name = self.getOutputName(content)
        filename = Path(str(self.save_folder)) / Path(str(output_name)).with_suffix(".mp3")
        print("start download ", filename, download_url)
        urllib.request.urlretrieve(download_url, filename)
        if(filename.is_file()):
            self.m_contents[index]["filename"] = str(filename)



    def main(self):
        for index, content in enumerate(self.m_contents):
            filename = content.get("filename", False)
            if not self.isFileExsite(filename):
                download_from = self.getUrlType(content.get("download_url"))
                if download_from == "youtube":
                   self.youtubeDl((index, content))
                elif download_from in ["direct_url", "gdrive"]:
                    self.direct_urlDl((index, content))
            else:
                print("file {} exite".format(filename))
        
        return self.m_contents
            

if __name__ == "__main__":
    content_links = [{"tags":{"artist": "zd", "title":"tb"}, "post_id": 21, "download_url":"https://docs.google.com/uc?export=download&id=1XF77sbvixZG0kUNYApHDsruBGd6g5Pm1"},
        {"artist": "jry", "title":"nju", "gdrive_upload_times":8, "filename":"X:\\workspace\\madoda-manager\\server.py" ,"post_id": 21, "download_links":["youtube.com/hgkjyuy"]}]
    dw = Download(content_links)
    print(dw.main())