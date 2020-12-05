import json
from pathlib import Path
from datetime import datetime

from .youtube import Youtube

class UploadList(Youtube):
    def __init__(self):
        super().__init__()
        self.__videos_to_upload_file = Path(str(self.main_youtube_path)) / str("videos_to_upload.json")
        self.__videos_uploaded = Path(str(self.main_youtube_path)) / str("videos_uploaded.json")
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
            
            if video_path:
                self.__videos_to_upload.append(m_content)
        self.__videos_to_upload_file.write_text(json.dumps(self.__videos_to_upload))


    def rm_video_from_upload_list(self, video_path):
        for index, video in enumerate(self.__videos_to_upload):
            if str( video.get("video_filename", "") ) == str(video_path):
                self.__videos_to_upload.pop(index)
        self.__videos_to_upload_file.write_text(json.dumps(self.__videos_to_upload))
    
    
    def add_to_complete_list(self, post_id, content): 
        if not self.__videos_uploaded.is_file():
            self.__videos_uploaded.write_text(json.dumps({}))
        
        try:
            videos_uploaded_text = self.__videos_uploaded.read_text()
            videos_uploaded = json.loads(videos_uploaded_text)
            videos_uploaded[post_id] = content
            self.__videos_uploaded.write_text(json.dumps(videos_uploaded))
        except:
            pass
       
            


    
    


class videoData():
    def __init__(self):
        self.td_year = datetime.today().year

    def get_data(self, m_content):
        yt_title = self.get_title(m_content)+" | Download MP3"
        data = {
            "snippet" : {
                "title": yt_title,
                "description": self.get_desc(m_content),
                "tags": self.get_tags(m_content),
                "categoryId": "10"
            },
            "status": {
                "privacyStatus":"public",
                "selfDeclaredMadeForKids": "false"
            }
        }

        return data

    
    def get_title(self, m_content):
        tags = m_content.get("tags", {})
        if tags.get("artist") or tags.get("title"):
            title = tags.get("artist", "MDDM") +" - "+ tags.get("title", "")
            if tags.get("sec_artists"):
                sec_artists =  ', '.join(map(str, tags.get("sec_artists")))
                title += " (Feat. {})".format(sec_artists)
            return title
 
        if m_content.get("video_filename"):
            title = Path(str(m_content.get("video_filename"))).stem
            return title
        
        return "MDDM NO TITLE"
    
    def get_desc(self, m_content):
        desc = ""
        tags = m_content.get("tags", {})
        if m_content.get("permalink"):
            desc+= "Baixar musica de "+self.get_title(m_content)
            desc += "\nDOWNLOAD MP3: "+m_content.get("permalink")+"\n"
        
        if tags.get("artist"):
            artist = tags.get("artist")
            if tags.get("sec_artists"):
                sec_artists =  ', '.join(map(str, tags.get("sec_artists")))
                artist += " (Feat. {})".format(sec_artists)
            desc += "\nArtist: "+artist
        
        if tags.get("title"):
            desc += "\nTitle: "+tags.get("title")


        desc += "\n\nmadoda music \nhttp://madodamusic.com/\n"
        return desc
    
    def get_tags(self, m_content):
        tags = m_content.get("tags", {})
        yt_title = self.get_title(m_content)
        yt_c_title_1 = yt_title + " download mp3"
        yt_c_title_2 = "Baixar " + yt_title
        yt_c_title_3 = "descarregar" + yt_title
        yt_tags = ["baixar musica", "download mp3", "descarregar musicas", yt_title, yt_c_title_1, yt_c_title_2, yt_c_title_3]
        artists = []
        if tags.get("artist"):
            artists.append(tags.get("artist"))
        
        if tags.get("sec_artists"):
            artists = artists + tags.get("sec_artists")
        
        
        for artist in artists:
            yt_tags.append(artist)
            yt_tags.append("baixar musicas de "+artist)
            yt_tags.append("baixar musicas de "+artist+ " de " +str(self.td_year))
            yt_tags.append(str(artist) + " download mp3")
        
        if tags.get("title"):
            yt_tags.append(tags.get("title"))
            yt_tags.append(tags.get("title")+" dwonload mp3")
        
        return yt_tags

        
        
        

        
        


if __name__ == "__main__":
    # upl = UploadList()
    # upl.add_videos_to_upload_list([{"title":"KB", "video_filename": "KDrive.mp4", "youtube_z-index":5}])
    # upl.rm_video_from_upload_list("Drive.mp4")
    # res = upl.get_videos_to_upload()
    # print(res)

    vd = videoData()
    m_content = {"permalink":"https://madodas/calema", "video_filename":"calema-sorte.mp4","tags":{"artist": "calema", "title":"sorte", "sec_artists":["lucas", "anita"]}}
    print(vd.get_data(m_content))