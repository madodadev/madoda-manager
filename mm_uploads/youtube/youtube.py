import json
from pathlib import Path

class Youtube():
    def __init__(self):
        self.main_path = Path(__file__).parent.parent.parent.absolute()
        self.main_youtube_path = self.main_path / Path("assets/youtube")
        self.main_youtube_path.mkdir(exist_ok=True)
        self.__main_conf_path = Path(str(self.main_path)) / str("assets/main_conf.json")
        self.__main_conf_key_name = "youtube"
        self.__conf = {}
        self.__init_conf()



    
    def __init_conf(self):
        if self.__main_conf_path.exists():
            conf = json.loads( self.__main_conf_path.read_text() )
            self.__conf = conf[self.__main_conf_key_name]

    
    
