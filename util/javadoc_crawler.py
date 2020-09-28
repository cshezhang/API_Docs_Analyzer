import sys

from util.log import logger
from requests_html import HTMLSession
from bs4 import BeautifulSoup


def main():
    target = "Sunshine"
    file = "E:/Code/" + target + "_allclasses.html"
    soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
    tag_list = soup.find_all()
    for tag in tag_list:
        # print(tag.name)
        if tag.name == 'a':
            # print(tag)
            link = tag['href']
            if not link.endswith(".html"):
                continue
            logger.info("Processing Link=" + str(link))
            session = HTMLSession()
            main_page = session.get(link)
            page_name = link.split("/")[-1]
            if main_page.status_code == 404:
                print("url open failed: {}".format(main_page.url))
                sys.exit()
            file = open("E:/Code/" + target + "/" + page_name, "wb")
            file.write(main_page.html.raw_html)
            file.close()


if __name__ == "__main__":
    main()
