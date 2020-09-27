import os


def get_first_layer_folders(dir_):
    # Not traveser the sub folders recursively, only traverse the layer files
    folders = []
    file_list = os.listdir(dir_)
    for i in range(0, len(file_list)):
        path = os.path.join(dir_, file_list[i])
        if os.path.isdir(path):
            folders.append(path)
    return folders


def get_first_layer_files(dir_):
    files = []
    file_list = os.listdir(dir_)
    for i in range(0, len(file_list)):
        path = os.path.join(dir_, file_list[i])
        if os.path.isfile(path):
            if ".html" in path:
                files.append(path)
    return files


def get_all_files(dir_):
    files_ = []
    list_ = os.listdir(dir_)
    for i in range(0, len(list_)):
        path = os.path.join(dir_, list_[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            if ".html" in path:
                files_.append(path)
    return files_
