import shutil
from os import path


class Zip_Folder:
    def __init__(self, folder_path: str):
        src = path.realpath(folder_path)
        root_dir, tail = path.split(src)
        shutil.make_archive("outputs", "zip", root_dir)
