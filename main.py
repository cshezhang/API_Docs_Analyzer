import os
import sys

from util.log import logger
from util.config import Config
from parsers.gms import GmsDocParser
from parsers.dex import DexFileParser
from parsers.java import JavaDocParser
from parsers.facebook import FacebookDocParser
from parsers.javalike import JavaLikeDocParser
from parsers.pushwoosh import PushwooshDocParser
from parsers.appbrain import AppbrainDocParser
from parsers.silverjava import SilverJavaDocParser
from util.traverseFolder import get_first_layer_folders, get_first_layer_files


def parse_facebook_folder(target_folder):
    logger.info("Facebook Doc Folder=" + target_folder)
    facebook_folders = get_first_layer_folders(target_folder)
    for facebook_doc in facebook_folders:
        logger.info("Processing Facebook Doc=" + facebook_doc)
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


def parse_javalike_doc(target_folder):
    logger.info("Javalike Doc Folder=" + target_folder)
    javalike_folders = get_first_layer_folders(target_folder)
    for javalike_doc in javalike_folders:
        logger.info("Processing Javalike Doc=" + javalike_doc)
        # print(javadoc)
        parser = JavaLikeDocParser(javalike_doc)
        parser.run()
        # parser.print_results()
        parser.print_to_csv()
        # break


def parse_javadoc_folder(target_folder):
    logger.info("Java Doc Folder=" + target_folder)
    javadoc_folders = get_first_layer_folders(target_folder)
    for javadoc in javadoc_folders:
        logger.info("Processing JavaDoc=" + javadoc)
        # print(javadoc)
        parser = JavaDocParser(javadoc)
        parser.run()
        # parser.print_results()
        parser.print_to_csv()
        # break


def parse_appbrain_doc(target_folder):
    logger.info("AppBrain Folder=" + target_folder)
    parser = AppbrainDocParser(target_folder)
    parser.run()
    # parser.print_results()
    parser.print_to_csv()


def parse_jar_folder(target_folder):
    logger.info("Jar Folder")
    if not os.path.isdir(target_folder):
        logger.error("Not a Folder! Exiting...")
        return
    jar_files = get_first_layer_files(target_folder, False)
    for jar_file in jar_files:
        logger.info("Processing File=" + jar_file)
        try:
            parser = DexFileParser(jar_file)
            parser.run()
            # parser.print_results()
            parser.print_to_csv()
        except Exception as e:
            print(e)


def parse_pushwoosh():
    logger.info('Pushwoosh')
    parser = PushwooshDocParser()
    parser.run()
    parser.print_results()


def parse_dex_folder(target_folder):
    logger.info("Dexs")
    logger.info(target_folder)
    files = get_first_layer_files(target_folder, False)
    # print(len(files))
    for file in files:
        try:
            logger.info("Processing File=" + file)
            parser = DexFileParser(file)
            parser.run()
            # parser.print_results()
            parser.print_to_csv()
        except Exception as e:
            print(e)


def parse_silverjava_doc():
    logger.info("Silver_Java_Doc")
    parser = SilverJavaDocParser()
    parser.run()
    parser.print_results()


def main():
    if not os.path.exists("./api_results"):
        os.mkdir("./api_results")
    parser_type = sys.argv[1]
    target_folder = sys.argv[2]
    Config.target_folder = target_folder
    if parser_type.lower() == 'jar_folder':
        parse_jar_folder(Config.target_folder)
    if parser_type.lower() == 'javadoc_folder':
        parse_javadoc_folder(target_folder)
    if parser_type.lower() == 'facebooks':
        parse_facebook_folder(target_folder)
    if parser_type.lower() == 'gms':
        parse_gms_folder()
    if parser_type.lower() == 'javalike_folder':
        parse_javalike_doc(target_folder)
    if parser_type.lower() == 'pushwoosh':
        parse_pushwoosh()
    if parser_type.lower() == "dexs":
        parse_dex_folder(target_folder)
    if parser_type.lower() == 'appbrain':
        parse_appbrain_doc()
    if parser_type.lower() == 'silverjava':
        parse_silverjava_doc()
    if parser_type.lower() == 'all_test':
        jar_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Jars"
        javadoc_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Java_Test"
        facebook_doc_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Facebook"
        javalike_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\Javalike"
        appbrain_folder = "C:\\Users\\Rainy\\Lab_Project\\dataset_science\\API_Docs\\Android_Docs\\AppBrain"
        parse_jar_folder(jar_folder)
        parse_javadoc_folder(javadoc_folder)
        parse_facebook_folder(facebook_doc_folder)
        parse_javalike_doc(javalike_folder)
        parse_appbrain_doc(appbrain_folder)
        # parse_silverjava_doc()
        # parse_pushwoosh()


if __name__ == '__main__':
    main()
