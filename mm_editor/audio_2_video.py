import os
from pathlib import Path
from datetime import datetime

from .make_image import MakeImage
class Audio2Video:
    def __init__(self, m_contents):
        self.m_contents = m_contents
        self.mkimg = MakeImage()
        self.main_folder = Path(__file__).parent.parent.absolute()
        self.main_videos_folder = self.main_folder / "assets/mm_editor/videos"
        self.videos_folder = self.main_videos_folder / datetime.today().strftime("%d_%m_%Y")
        self.videos_folder.mkdir(parents=True, exist_ok=True)



    def main(self):
        for index, m_content in enumerate(self.m_contents):
            filename = m_content.get("filename")
            if not filename:
                continue
            
            if not m_content.get("make_video") and not m_content.get("upload_to_youtube"):
                continue
            
            video_output = self.videos_folder / Path(str(filename)).stem
            video_output = video_output.with_suffix(".mp4")
            
            if video_output.is_file():
                self.m_contents[index]["video_filename"] = str(video_output.absolute())
                continue

            img_src = self.mkimg.get_image_src(m_content)
            
            print("start making video", datetime.now())
            cmd = '''ffmpeg -loop 1 -framerate 1 -i {img_i} -i {audio_i} -map 0:v -map 1:a -r 10 -vf "scale='iw-mod(iw,2)':'ih-mod(ih,2)',format=yuv420p" -movflags +faststart -shortest -fflags +shortest -max_interleave_delta 100M {video_O}'''.format(img_i=img_src, audio_i=filename, video_O=str(video_output.absolute()))
            # return cmd
            res = os.system(cmd)
            if res == 0:self.m_contents[index]["video_filename"] = str(video_output.absolute())
            print("end making video", datetime.now())
        
        return self.m_contents
                

if __name__ == "__main__":
    m_contents = [{"filename":"music.mp3", "upload_to_youtube":1}]
    a2v = Audio2Video(m_contents).main()
    print(a2v)

