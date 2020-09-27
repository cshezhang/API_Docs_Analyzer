# APIDoc_Analyzer is used to automatically extract sensitive API from docs.
# Senstive API is based on the related keyword.

import io
import sys
import csv
from bs4 import BeautifulSoup

from util.log import logger
from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_files, get_first_layer_folders


class GmsDocParser:

    def __init__(self):
        self.processing_class = ""
        self.sensitive_keywords = set()
        self.apis = []
        self.sensitive_apis = []

    def run(self):
        self.sensitive_keywords = get_sensitive_keywords()
        sum_tp = 0
        sum_fp = 0
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        api_folders = get_first_layer_folders(Config.target_folder)
        for api_folder in api_folders:
            (tp, fp) = self.process_api(api_folder)
            sum_tp = sum_tp + tp
            sum_fp = sum_fp + fp

    def process_api(self, folder):
        tp = 0
        fp = 0
        files_list = get_first_layer_files(folder)
        for i in range(0, len(files_list)):
            file = files_list[i]
            # logger.info("Processing File=" + str(file))
            self.processing_class = file.split("\\")[-1].split(" ")[0]
            logger.info("Current Class=" + self.processing_class)
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            tag_list = soup.find_all()
            (c_tp, c_fp) = self.get_privacy(tag_list)
            tp = tp + c_tp
            fp = fp + c_fp
        return tp, fp

    def get_privacy(self, tag_list):
        blacklist = ["head", "html", "path", "Throws"]
        table_list = []
        api_names = set()
        api2des = {}
        tp = 0
        fp = 0
        for i in range(0, len(tag_list)):
            tag = tag_list[i]  # tag is a table class used to parse method.
            if tag.name == 'table':
                if len(tag.find_all("tr")) <= 0 or len(tag.find_all("td")) <= 0:
                    continue
                title_name = ""  # title_name: The name of the title.
                for j in range(i - 1, -1, -1):  # Search for the table name.
                    pre_tag = tag_list[j]
                    if 'h' in pre_tag.name and pre_tag.name not in blacklist:
                        title_name = pre_tag.getText()
                        break
                if ("Method Summary" in title_name or "Field Summary" in title_name) and "Inherited" not in title_name:
                    table_list.append(tag)
                    # print("title_name=" + title_name)
                    # print("tag=" + str(tag))
                    tr_list = tag.find_all("tr")
                    for tr in tr_list:
                        td_list = tr.find_all("td")
                        if len(td_list) > 1:
                            target = td_list[1].getText().strip()
                            index = target.find('(')  # Split API parameters and name.
                            # Variable targets saves Field and Method.
                            api_name = target[: index]
                            api_names.add(api_name)
                            self.apis.append(api_name)
        descriptions = []
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            if 'h' in tag.name and tag.name not in blacklist:
                has_description = False
                target_api = ""
                for api_name in api_names:
                    if api_name in tag.getText():
                        has_description = True
                        target_api = api_name
                        break
                if has_description:
                    no = True
                    for j in range(i + 1, len(tag_list)):
                        next_tag = tag_list[j]
                        if next_tag.name == "p":
                            # if target_api in api2des.keys():
                            # print("What the fucking API!=" + target_api)
                            description = next_tag.getText()
                            api2des[target_api] = description
                            descriptions.append(description)
                            no = False
                            break
                    if no:
                        descriptions.append("No Description!")
        for api_name, description in api2des.items():
            is_sensitive = False
            privacy_item = ""
            for keywords in self.sensitive_keywords:
                is_sensitive = True
                # if keyword in description.lower() or keyword in api_name.lower():
                for keyword in keywords:  # 一个隐私项可能有多个keyword，比如Device_ID
                    if keyword.lower() not in api_name.lower():
                        is_sensitive = False
                if is_sensitive:
                    privacy_item = keywords
                    break
            if is_sensitive:
                self.sensitive_apis.add((self.processing_class, api_name, description, privacy_item))
                fp = fp + 1
                continue
            tp = tp + 1
        return tp, fp

    def print_results(self):
        print("--------------------------------------")
        for api in self.apis:
            print(api)
        print("**************************************")
        for sensitive_api in self.sensitive_apis:
            print(sensitive_api)
        print("--------------------------------------")
        print("API SUM=" + str(len(self.apis)))
        print("Sensitive API SUM=" + str(len(self.sensitive_apis)))

    def print_to_csv(self):
        with open("facebook.csv", "w") as csv_file:
            fieldnames = ["Class", "API_Name", "Description"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                writer.writerow(
                    {"Class": sensitive_api[0], "API_Name": sensitive_api[1], "Description": sensitive_api[2]}
                )
