from pathlib import Path

class MakeImage:
    def __init__(self):
        self.main_folder = Path(__file__).parent.parent.absolute()
        self.main_image_folder = self.main_folder / "assets/mm_editor/images"
        self.main_image_folder.mkdir(parents=True, exist_ok=True)

    
    def __make_image(self):
        img_src = self.main_image_folder / "mm_default.jpg"
        if img_src.is_file():
            return str(img_src.absolute())
        
        return False
    
    def get_image_src(self, m_content=None):
        return self.__make_image()


if __name__ == "__main__":
    mkimg = MakeImage()
    print(mkimg.get_image_src())