import os

def create_dir(pasta:str):
    dir_path = pasta
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path
