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


def main():
    parser_type = sys.argv[1]
    target_folder = sys.argv[2]
    Config.target_folder = target_folder
    if parser_type.lower() == 'facebook':
        logger.info("facebook")
        parser = FacebookDocParser()
        parser.run()
        parser.print_results()
        parser.print_to_csv()
    if parser_type.lower() == 'gms':
        logger.info('GMS')
        parser = GmsDocParser()
        parser.run()
        parser.print_results()
    if parser_type.lower() == 'java':
        logger.info('Java')
        parser = JavaDocParser()
        parser.run()
        parser.print_results()
    if parser_type.lower() == 'table':
        logger.info('Table')
        parser = TableDocParser()
        parser.run()
        parser.print_results()
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


if __name__ == '__main__':
    main()
