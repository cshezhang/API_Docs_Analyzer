import os
import zipfile
from shutil import copyfile


def get_first_layer_dirs(target_dir):
    dir_list = []
    current_list = os.listdir(target_dir)
    for i in range(0, len(current_list)):
        path = os.path.join(target_dir, current_list[i])
        if os.path.isdir(path):
            dir_list.append(path)
    return dir_list


def get_all_files(target_dir):
    file_list = []
    list_ = os.listdir(target_dir)
    for i in range(0, len(list_)):
        path = os.path.join(target_dir, list_[i])
        if os.path.isdir(path):
            file_list.extend(get_all_files(path))
        if os.path.isfile(path):
            file_list.append(path)
    return file_list


def dexClean(target_dir):
    file_list = get_all_files(target_dir)
    for file in file_list:
        if "javadoc" not in file:
            print(file)
            os.remove(file)


# def process_jar(target_folders):
#     for folder in target_folders:
#         file_list = get_all_files(folder)
#         hasAar = False
#         aar_file = ""
#         for file in file_list:
#             if ".aar" in file:
#                 hasAar = True
#                 aar_file = file
#             if ".jar" in file:
#                 jar_file = file
#         print(aar_file)
#         print(jar_file)


def extract_jar_files():
    # out_dir specifies the source folder of different package files, including .jar or .aar
    out_dir = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\jar_source"
    folder_list = get_first_layer_dirs(out_dir)
    jar_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\jars"
    if not os.path.exists(jar_folder):
        os.mkdir(jar_folder)
    for folder in folder_list:
        sdk_name = folder.split("\\")[-1]
        file_list = get_all_files(folder)
        hasAAR = False
        aar_pathes = []
        jar_pathes = []
        for file in file_list:
            if file.endswith(".aar"):
                hasAAR = True
                aar_pathes.append(file)
            if file.endswith(".jar"):
                jar_pathes.append(file)
        source_files = []
        # print("Has AAR File=" + str(hasAAR))
        if hasAAR:
            for aar_path in aar_pathes:
                print(aar_path)
                aar_file = zipfile.ZipFile(aar_path, "r")
                extract_path = aar_path[:-4]
                aar_file.extractall(extract_path)
                jar_file = extract_path + os.sep + "classes.jar"
                dst_file = extract_path + os.sep + extract_path.split("\\")[-1] + ".jar"
                if not os.path.exists(dst_file):
                    os.rename(jar_file, dst_file)
                source_files.append(dst_file)
        else:
            source_files = jar_pathes
        new_sdk_folder = jar_folder + os.sep + sdk_name
        print("New SDK Folder=" + new_sdk_folder)
        print("Source File Length=" + str(len(source_files)))
        if not os.path.exists(new_sdk_folder):
            os.mkdir(new_sdk_folder)
        for source_file in source_files:
            file_name = source_file.split("\\")[-1]
            target_file = new_sdk_folder + os.sep + file_name
            if not os.path.exists(target_file):
                print("Source File=" + source_file)
                print("Target File=" + target_file)
                copyfile(source_file, target_file)


def extract_javadoc_files():
    out_dir = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\SDK_crawl"
    folder_list = get_first_layer_dirs(out_dir)
    for folder in folder_list:
        sdk_name = folder.split("\\")[-1]
        file_list = get_all_files(folder)
        hasJavadoc = False
        for file in file_list:
            if "javadoc" in file:
                hasJavadoc = True
                break
        if not hasJavadoc:
            # print(sdk_name)
            continue
        print("Javadoc SDK Name=" + str(sdk_name))
        target_dir = out_dir + os.sep + "javadocs"
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        target_dir += os.sep + sdk_name
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        for srcFile in file_list:
            if "javadoc" in srcFile and (srcFile.endswith(".jar") or srcFile.endswith(".aar")):
                fileName = srcFile.split("\\")[-1]
                targetFile = target_dir + os.sep + fileName
                print("Source File=" + srcFile)
                print("Target File=" + targetFile)
                if not os.path.exists(targetFile):
                    copyfile(srcFile, targetFile)


def processGA():
    target_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\History\\javadoc\\Game_Analytics_Jar"
    folders = get_first_layer_dirs(target_folder)
    for folder in folders:
        file_list = get_all_files(folder)
        jar_file = ""
        file_name = folder.split("\\")[-1]
        for file in file_list:
            if file.endswith(".jar"):
                jar_file = file
                target_file = target_folder + os.sep + file_name + "_" + file.split("\\")[-1]
                print(target_file)
                copyfile(jar_file, target_file)


if __name__ == "__main__":
    extract_jar_files()
    # extract_javadoc_files()