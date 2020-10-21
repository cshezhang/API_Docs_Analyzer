import os


def get_first_layer_folders(target_dir):
    # Not traveser the sub folders recursively, only traverse the layer files
    folders = []
    file_list = os.listdir(target_dir)
    for i in range(0, len(file_list)):
        path = os.path.join(target_dir, file_list[i])
        if os.path.isdir(path):
            folders.append(path)
    return folders


def get_second_layer_files(dir_, html=True):
    files = []
    file_list = os.listdir(dir_)
    for i in range(0, len(file_list)):
        path = os.path.join(dir_, file_list[i])
        if os.path.isdir(path):
            files.append(get_first_layer_files(path, html))
    return files


def get_first_layer_files(dir_, html=True):
    files = []
    file_list = os.listdir(dir_)
    for i in range(0, len(file_list)):
        path = os.path.join(dir_, file_list[i])
        if os.path.isfile(path):
            if html:
                if ".html" in path:
                    files.append(path)
            else:
                files.append(path)
    return files


def get_all_files_in_javadoc(dir_):
    files_ = []
    list_ = os.listdir(dir_)
    for i in range(0, len(list_)):
        path = os.path.join(dir_, list_[i])
        if os.path.isdir(path):
            files_.extend(get_all_files_in_javadoc(path))
        if os.path.isfile(path):
            if "-" not in path and ".html" in path:
                files_.append(path)
    return files_


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
