import os
import zipfile

from util.log import logger
from shutil import copyfile
from parsers.gms import GmsDocParser
from parsers.dex import DexFileParser
from parsers.java import JavaDocParser
from parsers.facebook import FacebookDocParser
from parsers.javalike import JavaLikeDocParser
from parsers.pushwoosh import PushwooshDocParser
from parsers.appbrain import AppbrainDocParser
from parsers.silverjava import SilverJavaDocParser
from util.traverseFolder import get_first_layer_folders, get_first_layer_files, get_all_files


def parse_facebook_folder(target_folder):
    # logger.info("Facebook Doc Folder=" + target_folder)
    facebook_folders = get_first_layer_folders(target_folder)
    for facebook_doc in facebook_folders:
        # logger.info("Processing Facebook Doc=" + facebook_doc)
        parser = FacebookDocParser(facebook_doc)
        parser.run()
        # parser.print_results()
        parser.print_to_csv()


def parse_gms_folder():
    logger.info('GMS')
    parser = GmsDocParser()
    parser.run()
    parser.print_results()
    parser.print_to_csv()


def parse_javalike_doc(target_folder, sdk_name):
    # logger.info("Javalike Doc Folder=" + target_folder)
    javalike_folders = get_first_layer_folders(target_folder)
    for javalike_doc in javalike_folders:
        # logger.info("Processing Javalike Doc=" + javalike_doc.split("\\")[-1])
        doc_name = javalike_doc.split("\\")[-1]
        print(doc_name)
        parser = JavaLikeDocParser(javalike_doc, sdk_name)
        parser.run()
        # parser.print_results()
        parser.print_to_csv()


def parse_javadoc_folder(sdk_name, target_folder):
    print("SDK Name=" + sdk_name + "  Java Doc Folder=" + target_folder)
    javadoc_folders = get_first_layer_folders(target_folder)
    for javadoc in javadoc_folders:
        print("Processing JavaDoc=" + javadoc.split("\\")[-1])
        # print(javadoc)
        parser = JavaDocParser(sdk_name, javadoc)
        parser.run()
        parser.print_results()
        parser.print_to_csv()


def parse_appbrain_doc(target_folder):
    # logger.info("AppBrain Folder=" + target_folder)
    parser = AppbrainDocParser(target_folder)
    print("AppBrain")
    parser.run()
    # parser.print_results()
    parser.print_to_csv()


def parse_jar_folder(sdk_name, target_folder):
    # logger.info("Jar Folder=" + target_folder)
    jar_files = get_first_layer_files(target_folder, False)
    for jar_file in jar_files:
        if not jar_file.endswith(".jar"):
            continue
        jar_name = jar_file.split(os.sep)[-1]
        print(jar_file.split("\\")[-1])
        # logger.info("Processing File=" + jar_file)
        try:
            parser = DexFileParser(sdk_name, jar_file)
            parser.run()
            parser.print_results()
            parser.print_to_csv()
        except Exception as e:
            print(jar_name + " meets exception!")
            print(e)


def parse_pushwoosh():
    logger.info('Pushwoosh')
    parser = PushwooshDocParser()
    parser.run()
    parser.print_results()


def parse_dex_folder(target_folder):
    logger.info("Dex Folder=" + target_folder)
    files = get_first_layer_files(target_folder, False)
    # print(len(files))
    for file in files:
        try:
            parser = DexFileParser(file)
            parser.run()
            # parser.print_results()
            parser.print_to_csv()
        except Exception as e:
            print(e)


def parse_silverjava_doc(target_folder):
    silverjava_folders = get_first_layer_folders(target_folder)
    for doc_folder in silverjava_folders:
        print("Processing Silver Java Doc=" + doc_folder.split(os.sep)[-1])
        # print(javadoc)
        parser = SilverJavaDocParser(doc_folder)
        parser.run()
        # parser.print_results()
        parser.print_to_csv()


def process_results():
    result_folders = get_first_layer_folders("." + os.sep + "api_results")
    csv_cnt = 0
    loss = 0.0
    for res_folder in result_folders:
        csv_files = get_first_layer_files(res_folder, html=False)
        for csv_file in csv_files:
            csv = open(csv_file, "r", encoding="utf-8")
            # print(csv_file)
            lines = csv.readlines()
            csv_name = csv_file.split(os.sep)[-1][:-4]
            sum_cnt = 0
            general_cnt = 0
            for line in lines:
                if "," in line:
                    sum_cnt = sum_cnt + 1
                if "logevent" in line or "GeneralLogEvent" in line or "trackEvent" in line or \
                        "GeneralUserProperty" in line:
                    general_cnt = general_cnt + 1
            if sum_cnt >= 0:
                if general_cnt >= 0:
                    csv_cnt = csv_cnt + 1
                    print(csv_name + "," + str(sum_cnt) + "," + str(general_cnt))
                    # loss = loss + (sum_cnt - general_cnt) / sum_cnt


def process_jar_package_folder(target_folder):
    sdk_name = target_folder.split(os.sep)[-1]
    parse_jar_folder(sdk_name, target_folder)


def process_javadoc_package_folder(target_folder):
    file_list = get_first_layer_files(target_folder, html=False)
    java_doc_folders = []
    new_folder_path = target_folder + os.sep + "new_sdks"
    for file in file_list:
        if ".jar" in file:
            # print("File=" + file)
            zip_file = zipfile.ZipFile(file, "r")
            sdk_name = file.split(os.sep)[-1][:-4]
            # print("SDK_Name=" + sdk_name)
            folder_path = file[0:file.rfind(os.sep)]
            # print("Folder_Path=" + folder_path)
            extract_path = folder_path + os.sep + sdk_name
            # print("Extract_Path=" + extract_path)
            zip_file.extractall(extract_path)
            file_list = get_all_files(extract_path, html=True)
            # print(extract_path)
            black_list = ["allclasses", "constant-values", "deprecated-list", "help-doc", "index", "overview-", "package-"]
            html_list = []
            for html_file in file_list:
                file_name = html_file.split("\\")[-1]
                neglect = False
                for prefix in black_list:
                    if file_name.startswith(prefix):
                        neglect = True
                        break
                if neglect:
                    continue
                html_list.append(html_file)
            new_sdk_folder = new_folder_path + os.sep + sdk_name + "_new"
            next_folder = new_sdk_folder + os.sep + "All"
            # print("new_folder=" + new_sdk_folder)
            # print("next_folder=" + next_folder)
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)
            if not os.path.exists(new_sdk_folder):
                os.mkdir(new_sdk_folder)
            if not os.path.exists(next_folder):
                os.mkdir(next_folder)
            for html_file in html_list:
                html_name = html_file.split(os.sep)[-1]
                copyfile(html_file, next_folder + os.sep + html_name)
            java_doc_folders.append(new_sdk_folder)
    parse_javadoc_folder(new_folder_path.split("\\")[-2], new_folder_path)


def main():
    javadoc_folders = get_first_layer_folders("C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\History\\javadocs")
    for javadoc_folder in javadoc_folders:
        print("Processing Folder=" + javadoc_folder)
        process_javadoc_package_folder(javadoc_folder)
    # jar_folders = get_first_layer_folders("C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\History\\jars")
    # for jar_folder in jar_folders:
    #     print("Processing Jar Folder=" + jar_folder)
    #     process_jar_package_folder(jar_folder)
    # if not os.path.exists("./api_results"):
    #     os.mkdir("./api_results")
    # parser_type = sys.argv[1]
    # target_folder = sys.argv[2]
    # Config.target_folder = target_folder
    # if parser_type.lower() == 'jar_folder':
    #     parse_jar_folder(target_folder)
    # if parser_type.lower() == 'javadoc_folder':
    #     parse_javadoc_folder(target_folder)
    # if parser_type.lower() == 'facebooks':
    #     parse_facebook_folder(target_folder)
    # if parser_type.lower() == 'gms':
    #     parse_gms_folder()
    # if parser_type.lower() == 'javalike_folder':
    #     parse_javalike_doc(target_folder)
    # if parser_type.lower() == 'pushwoosh':
    #     parse_pushwoosh()
    # if parser_type.lower() == "dexs":
    #     parse_dex_folder(target_folder)
    # if parser_type.lower() == 'appbrain':
    #     parse_appbrain_doc(target_folder)
    # if parser_type.lower() == 'silverjava':
    #     parse_silverjava_doc()
    # if parser_type.lower() == 'all_test':
    #     jar_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\jar_test"
    #     javadoc_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Java_Test"
    #     facebook_doc_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Facebook"
    #     javalike_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Javalike"
    #     appbrain_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\AppBrain"
    #     silverjava_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Silverjava"
    #     parse_jar_folder(jar_folder)
    #     parse_javadoc_folder(javadoc_folder)
    #     parse_facebook_folder(facebook_doc_folder)
    #     parse_javalike_doc(javalike_folder)
    #     parse_appbrain_doc(appbrain_folder)
    #     parse_silverjava_doc(silverjava_folder)
    #     parse_pushwoosh()
    # process_results()


if __name__ == '__main__':
    main()
