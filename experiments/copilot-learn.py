import os
import shutil


def rename_file(first_file=None, new_file_name=None):
    folder_path = "../pages/video"
    print(os.getcwd())

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Directory {folder_path} does not exist.")

    old_file_path = os.path.join(folder_path, first_file)
    if not os.path.exists(old_file_path):
        raise FileNotFoundError(f"File {old_file_path} does not exist.")

    new_file_path = os.path.join(folder_path, new_file_name)
    os.rename(old_file_path, new_file_path)

    shutil.copy2(new_file_path, "../pages/")
    return new_file_path


rename_file(first_file="video.mp4", new_file_name="video_long.mp4")
