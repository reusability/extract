import shutil


class Zip_Folder:
    def __init__(self, folder_path: str):
        shutil.make_archive("outputs", "zip", folder_path)
