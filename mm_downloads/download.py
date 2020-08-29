from pathlib import Path
from datetime import datetime

from .youtube import YoutubeDownload
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
        sites = {"youtube":"https://www.youtube.com/"}
        for index, site in sites.items():
            if url.startswith(site.lower()):
                return index
        
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
        tags = content.get("tags")
        if tags:
            name = self.getNameByTags(tags)
            if name:
                return Path(str(self.save_folder)) /  Path(str(name))
        return False

    def youtubeDl(self, m_content):
        index, content = m_content
        download_url = content.get("download_url")
        yt_download = YoutubeDownload()
        output_name = self.getOutputName(content)
        filename = yt_download.mp3(download_url, output_name)
        self.m_contents[index]["filename"] = str(filename)

    
    def main(self):
        for index, content in enumerate(self.m_contents):
            filename = content.get("filename", False)
            if not self.isFileExsite(filename):
                download_from = self.getUrlType(content.get("download_url"))
                if download_from == "youtube":
                   self.youtubeDl((index, content))
            else:
                print("file {} exite".format(filename))
        
        return self.m_contents
            

if __name__ == "__main__":
    content_links = [{"tags":{"artist": "zd", "title":"tb"}, "post_id": 21, "download_url":"https://www.youtube.com/voikvjo"},
        {"artist": "jry", "title":"nju", "gdrive_upload_times":8, "filename":"X:\\workspace\\madoda-manager\\server.py" ,"post_id": 21, "download_links":["youtube.com/hgkjyuy"]}]
    dw = Download(content_links)
    # print( dw.getUrlType(" https://www.Youtube.com/") )
    # print(content_links[0], "\n")
    # for index, x in enumerate(content_links):
    #     print(x, index)
    print(dw.m_contents, "\n\n")
    dw.main()
    print("\n\n", dw.m_contents)

    # Path("X:\\workspace\\madoda-manager\\server\lm").mkdir(False)
    print(Path("X:\\workspace\\madoda-manager\\"))