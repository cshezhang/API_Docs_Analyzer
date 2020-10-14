import os


def check_api(temp_api):
    black_list = ["getServerName", "getThreadName", "setServerName", "setThreadName", "TextHeight", "TimeInSecond",
                  "TimeInMillisecond", "TimeInterval", "requestPasswordReset", "LocationProvider", "DisplayHeight",
                  "DisplayWidth", "LocationAttribute", "TimeIn", "getDeviceScreenWidthDip",
                  "getDeviceWidth", "createLocationRequest", "addBusinessEventWithCurrency", "emptyLocationData"]
    # black_list.append("")
    # black_list.append("")
    # black_list.append("")
    api = temp_api.lower()
    if api == 'getage' or api == 'setage':
        return True
    # if not (api.startswith("get") or api.startswith("set")):
    #     return False
    if "location" in api and not ("get" not in api and "set" not in api):
        return False
    if "click" in api and "onclick" not in api:
        return False
    start_words = ["waitfor", "doNotRead", "maybe", "to", "clear", "config", "setis", "setneed", "onreceive", "onreceive", "handle", "unset", "delete", "stop", "Notify", "trigger", "warn", "use"]
    end_words = ["TimeImmediately", "Callback", "Format", "num", "space", "Configeration", "source", "type", "purpose", "option", "report", "area", "Reset", "Surpport", "Configuration", "Mode", "Describe", "disabled", "Clickable", "Notify"]
    for word in start_words:
        if api.startswith(word.lower()):
            return False
    for word in end_words:
        if api.endswith(word.lower()):
            return False
    for word in black_list:
        if word.lower() in api:
            return False
    if api.startswith("from") or api.startswith("check") or api.startswith("disable"):
        return False
    if api.startswith("has") or api.startswith("search") or api.startswith("enable"):
        return False
    if api.startswith("calculate") or api.startswith("is") or api.startswith("remove"):
        return False
    if api.endswith("handler") or api.endswith("strategy") or api.endswith("support"):
        return False
    if api.endswith("enabled") or api.endswith("listener") or api.endswith("protocal"):
        return False
    return True


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
