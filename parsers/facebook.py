# APIDoc_Analyzer is used to automatically extract sensitive API from Facebook-style Docs.
# Senstive API is based on the related keyword.

import os
import csv
from bs4 import BeautifulSoup

from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_folders, get_first_layer_files
from util.MethodChecker import filter_api, check_api_by_class


class FacebookDocParser:

    def __init__(self, target_folder=""):
        self.processing_class = ""
        self.sensitive_keywords = set()
        self.apis = []
        self.sensitive_apis = []
        if target_folder == "":
            self.api_folders = get_first_layer_folders(Config.target_folder)
        else:
            self.api_folders = get_first_layer_folders(target_folder)

    def run(self):
        self.sensitive_keywords = get_sensitive_keywords()
        sum_tp = 0
        sum_fp = 0
        for api_folder in self.api_folders:
            (tp, fp) = self.process_api(api_folder)
            sum_tp = sum_tp + tp
            sum_fp = sum_fp + fp

    def process_api(self, folder):
        tp = 0
        fp = 0
        files_list = get_first_layer_files(folder)
        for i in range(0, len(files_list)):
            file = files_list[i]
            self.processing_class = file.split("\\")[-1].split(" ")[0]
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            tag_list = soup.find_all()
            (c_tp, c_fp) = self.get_privacy(tag_list)
            tp = tp + c_tp
            fp = fp + c_fp
        return tp, fp

    def get_privacy(self, tag_list):
        api2des = {}
        tp = 0
        fp = 0
        method_tag = False
        full_class_name = ""
        for tag in tag_list:
            if tag.name == "li":
                txt = tag.getText()
                if "com.facebook" in txt:
                    full_class_name = tag.getText()
        for i in range(0, len(tag_list)):
            tag = tag_list[i]  # tag is a table class used to parse method.
            if tag.name == "span" and "Method Summary" in tag.getText():
                method_table = tag_list[i + 1].find_all()
                first = True
                for row in method_table:
                    if row.name != "tr":
                        continue
                    if first:
                        first = False
                        continue
                    columns = row.find_all()
                    for column in columns:
                        if column.name == "td":
                            api = column.getText()
                            left = api.find("(")
                            if left != -1:
                                self.apis.append(api[: left])
            if "Method Detail" in tag.getText():
                method_tag = True
            if method_tag and tag.name == "h4" and tag.getText() in self.apis:
                if len(tag_list[i + 3].getText()) > len(tag_list[i + 2].getText()):
                    des = tag_list[i + 3].getText()
                else:
                    des = tag_list[i + 2].getText()
                api2des[tag.getText()] = des
        for api_name, description in api2des.items():
            is_sensitive, privacy_item = check_api_by_class(full_class_name, api_name)
            if is_sensitive:
                description = description.replace("\n", " ")
                self.sensitive_apis.append((full_class_name, api_name, description, privacy_item))
                fp = fp + 1
                continue
            tp = tp + 1
        return tp, fp

    def print_results(self):
        # print("--------------------------------------")
        # for api in self.apis:
        #     print(api)
        # print("**************************************")
        # for sensitive_api in self.sensitive_apis:
        #     print(sensitive_api)
        # print("--------------------------------------")
        print("API SUM=" + str(len(self.apis)) + "  Sensitive API SUM=" + str(len(self.sensitive_apis)))

    def print_to_csv(self):
        if not os.path.exists(".\\api_results\\facebook\\"):
            os.mkdir(".\\api_results\\facebook")
        csv_name = ".\\api_results\\facebook\\" + self.api_folders[0].split("\\")[-2] + ".csv"
        # print("CSV_Name=" + csv_name)
        sensitive_cnt = 0
        with open(csv_name, "w", encoding='utf-8') as csv_file:
            fieldnames = ["Class", "API_Name", "Description"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                if filter_api(sensitive_api[1]):
                    writer.writerow({"Class": sensitive_api[0], "API_Name": sensitive_api[1],
                                     "Description": sensitive_api[2]})
                    sensitive_cnt = sensitive_cnt + 1
        print("Sensitive API SUM=" + str(sensitive_cnt))