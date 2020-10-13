from __future__ import unicode_literals
import youtube_dl
from pathlib import Path

class YoutubeDownload:
    def __init__(self, save_folder=None):
        if save_folder:
            self.save_folder = save_folder
        else:
            self.save_folder = Path(__file__).absolute().parent.parent / Path("musics")

   
   
    def mp3(self, yt_url, save_as= None):
        if save_as:
           title = save_as
        else:
            title = '%(title)s'
  
        for num in range(0, 5):
            try:
                ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.save_folder)+'/'+str(title)+'.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                }
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(yt_url, download=True)
                    if title == "%(title)s":
                        return Path(self.save_folder) / Path(meta['title']).with_suffix(".mp3")
                    else:
                        return Path( str(self.save_folder) ) / Path(str(title)).with_suffix(".mp3")
                            
                break
            except youtube_dl.utils.DownloadError:
                pass

if __name__ == "__main__":
    yt = YoutubeDownload()
    links = ["https://www.youtube.com/watch?v=m0mC3dcAOFU"]
    for lin in links:
        print(yt.mp3(lin, "matias - teu olhar"))
