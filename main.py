import os
import sys

from util.log import logger
from util.config import Config
from parsers.gms import GmsDocParser
from parsers.dex import DexFileParser
from parsers.java import JavaDocParser
from parsers.facebook import FacebookDocParser
from parsers.table import TableDocParser
from parsers.javalike import JavaLikeDocParser
from parsers.pushwoosh import PushwooshDocParser
from parsers.appbrain import AppbrainDocParser
from parsers.silverjava import SilverJavaDocParser
from util.traverseFolder import get_first_layer_folders, get_first_layer_files


def main():
    parser_type = sys.argv[1]
    target_folder = sys.argv[2]
    Config.target_folder = target_folder
    if parser_type.lower() == 'jar_folder':
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
                parser.print_results()
                # parser.print_to_csv()
            except Exception as e:
                print(e)
    if parser_type.lower() == 'javadoc_folder':
        logger.info("Java Doc Folder=" + target_folder)
        if not os.path.isdir(target_folder):
            logger.error("Not a Folder! Exiting...")
            return
        javadoc_folders = get_first_layer_folders(target_folder)
        for javadoc in javadoc_folders:
            logger.info("Processing JavaDoc=" + javadoc)
            # print(javadoc)
            parser = JavaDocParser(javadoc)
            parser.run()
            # parser.print_results()
            parser.print_to_csv()
            # break
    if parser_type.lower() == 'facebooks':
        logger.info("Facebook Docs")
        facebook_folders = get_first_layer_folders(target_folder)
        for facebook_doc in facebook_folders:
            logger.info("Processing Facebook Doc=" + facebook_doc)
            # print(javadoc)
            parser = FacebookDocParser(facebook_doc)
            parser.run()
            # parser.print_results()
            parser.print_to_csv()
            # break
    if parser_type.lower() == 'facebook':
        logger.info("Facebook")
        parser = FacebookDocParser()
        parser.run()
        parser.print_results()
        parser.print_to_csv()
    if parser_type.lower() == 'gms':
        logger.info('GMS')
        parser = GmsDocParser()
        parser.run()
        parser.print_results()
        parser.print_to_csv()
    if parser_type.lower() == 'java':
        logger.info('Java')
        parser = JavaDocParser()
        parser.run()
        parser.print_results()
        parser.print_to_csv()
    if parser_type.lower() == 'table':
        logger.info('Table')
        parser = TableDocParser()
        parser.run()
        parser.print_results()
    if parser_type.lower() == 'javalikes':
        logger.info("Javalike Docs")
        javalike_folders = get_first_layer_folders(target_folder)
        for javalike_doc in javalike_folders:
            logger.info("Processing Facebook Doc=" + javalike_doc)
            # print(javadoc)
            parser = JavaLikeDocParser(javalike_doc)
            parser.run()
            # parser.print_results()
            parser.print_to_csv()
            # break
    if parser_type.lower() == 'javalike':
        logger.info('Java-like')
        parser = JavaLikeDocParser()
        parser.run()
        parser.print_results()
    if parser_type.lower() == 'pushwoosh':
        logger.info('Pushwoosh')
        parser = PushwooshDocParser()
        parser.run()
        parser.print_results()
    if parser_type.lower() == 'dex':
        logger.info("Dex")
        parser = DexFileParser(target_folder)
        parser.run()
        parser.print_results()
        parser.print_to_csv()
    if parser_type.lower() == "dexs":
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
    if parser_type.lower() == 'appbrain':
        logger.info("AppBrain")
        parser = AppbrainDocParser()
        parser.run()
        parser.print_results()
        parser.print_to_csv()
    if parser_type.lower() == 'silverjava':
        logger.info("Appsfire")
        parser = SilverJavaDocParser()
        parser.run()
        parser.print_results()


if __name__ == '__main__':
    main()
