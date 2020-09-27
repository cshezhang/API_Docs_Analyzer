
class Config:

    j2d_path = "D:\\tools\\dex2jar-2.0\\d2j-jar2dex.bat"

    dx_path = "C:\\Users\\nofaker\\AppData\\Local\\Android\\Sdk\\build-tools\\29.0.2\\dx.bat"

    target_folder = ""

    filter_keywords = [
        "personal data",
        "data type",
        "information about you",
        "your information",
        "collect information",
        "information about",
        "*info",
        "address",
        "data request",
        "data send"
    ]

    synonym = {
        "click": ["hit"],
        "preference": ["hobby", "favorite", "favourite"]
    }

    def set_target_folder(self, target_folder):
        self.target_folder = target_folder