import eyed3 
import os
from datetime import datetime
from pathlib import Path
import json
class EditTags:
    def __init__(self, m_contents):
        self.m_contents = m_contents
        self.main_path = Path(__file__).parent.parent.absolute()
        
        imagepath = Path(__file__).parent / "image.jpg"
        if imagepath.exists():
            self.main_image = imagepath.read_bytes()
        else:
            self.main_image = False
    
    
    def edit_tags_by_tag_data(self,filename, tag_data):
        print("editing tags td", filename)
        try:
            tag_data = {str(index).lower():str(val) for index, val in tag_data.items()}
            # print(tag_keys)
            audiofile = eyed3.load(filename)
            audiofile.initTag()            
            if "image" in tag_data.keys():
                imagedata = Path(str(tag_data["Image"])).read_bytes()
                audiofile.tag.images.set(3,imagedata,"image/jpeg",u"madoda music")
            elif self.main_image:
                print("main image")
                audiofile.tag.images.set(3,self.main_image,"image/jpeg",u"madoda music")
                
            if "artist" in tag_data.keys():
                audiofile.tag.artist = tag_data["artist"]
            
            if "title" in tag_data.keys():
                audiofile.tag.title = tag_data["title"]
            
            if "album" in tag_data.keys():
                audiofile.tag.album = tag_data["album"]
            else:
                audiofile.tag.album = u"madoda music"
            
            # audiofile.tag.setTextFrame = "post_id"
            audiofile.tag.post_id = "45"
            print(dir(audiofile.tag.comments))
            print(audiofile.tag.comments.remove(""))
            audiofile.tag.comments 
            audiofile.tag.version = (2, 3, 0)
            audiofile.tag.save()
        except:
            print("error editing tags")
        

    def tags_by_file_name(self, filename):
        print("editing tags ", filename)
        try:
            audiofile = eyed3.load(filename)
            audiofile.initTag()
            if self.main_image:
                audiofile.tag.images.set(3,self.main_image,"image/jpeg",u"madoda music")
            
            audiofile.tag.title = str(Path(str(filename)).stem)
            audiofile.tag.album = u"madoda music"
            audiofile.tag.version = (2, 3, 0)
            audiofile.tag.save()
        except:
            print("error editing tag ", filename)


    def edit(self):
        for index, content in enumerate(self.m_contents):
            filename = content.get("filename")
            if filename:
                if Path(str(filename)).exists() and Path(str(filename)).suffix == ".mp3":
                    tags = content.get("tags")
                    if tags:
                        self.edit_tags_by_tag_data(filename, tags)
                    else:
                        self.tags_by_file_name(filename) 
                    # {}.setdefault("last_modificacion", datetime.now())         


if __name__ == "__main__":
    content = [{'tags': {'Artist': 'zd', 'title': 'tb'}, 'post_id': 21, 'download_url': 'https://www.youtube.com/voikvjo', 'filename': 'X:\workspace\madoda-manager\musics\Dj Black Spygo - Só Tu (feat. Aurora Ferreira & Edgar Domingos).mp3'}, {'artist': 'jry', 'title': 'nju', 'filename': 'X:\\workspace\\madoda-manager\\server.py', 'post_id': 21, 'download_links': ['youtube.com/hgkjyuy']}]
    ed = EditTags(content)
    print( ed.edit() )
    tags_data = content[0]["tags"]
    tags_data = {str(index).lower():str(val) for index, val in tags_data.items()}
    print(tags_data)