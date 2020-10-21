class Config:
    javadoc_folder_path = "~\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Java"
    jar_folder_path = "~\\Lab_Project\\dataset_science\\API_Docs\\Android_Jars"

    dx_path = "C:\\Users\\Rainy\\AppData\\Local\\Android\\Sdk\\build-tools\\30.0.0\\dx.bat"

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
