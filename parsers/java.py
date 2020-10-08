# Java_Doc_Analyzer is used to automatically extract sensitive APIs from java-style api docs.
# Senstive API is based on the related keyword match.

import io
import sys
import csv
from bs4 import BeautifulSoup

from util.log import logger
from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_files, get_first_layer_folders


class JavaDocParser:

    def __init__(self):
        self.processing_class = ""
        self.full_class_name = ""
        self.sensitive_keywords = set()
        self.apis = []
        self.sensitive_apis = []

    def run(self):
        self.sensitive_keywords = get_sensitive_keywords()
        print(self.sensitive_keywords)
        sum_tp = 0
        sum_fp = 0
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        api_folders = get_first_layer_folders(Config.target_folder)
        for api_folder in api_folders:
            logger.info("Processing Folder:" + str(api_folder))
            (tp, fp) = self.process_api(api_folder)
            sum_tp = sum_tp + tp
            sum_fp = sum_fp + fp
        # print("SUM_TP=" + str(sum_tp))
        # print("SUM_FP=" + str(sum_fp))

    def process_api(self, folder):
        tp = 0
        fp = 0
        files_list = get_first_layer_files(folder)
        for i in range(0, len(files_list)):
            file = files_list[i]
            self.processing_class = file.split("\\")[-1].split(" ")[0]
            # We should consider the full class name here.
            logger.info("Processing Class=" + self.processing_class)
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            tag_list = soup.find_all()
            full_name_find = False
            for j in range(0, len(tag_list)):
                tag = tag_list[j]
                if tag.name == "h2":
                    next_tag = tag_list[j - 1]
                    self.full_class_name = next_tag.getText() + "." + self.processing_class[ : -5]
                    break
                if full_name_find:
                    break
            logger.info("FULL_CLASS_NAME=" + self.full_class_name)
            c_tp, c_fp = self.get_privacy(tag_list)
            tp = tp + c_tp
            fp = fp + c_fp
        return tp, fp

    def get_privacy(self, tag_list):
        api_names = set()
        api2des = {}
        api2signature = {}
        tp = 0
        fp = 0
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            is_method_section = False
            if tag.name == 'h3':
                des_text = tag.getText()
                if "Method Detail" in des_text or "方法详细资料" in des_text or "メソッドの詳細" in des_text:
                    is_method_section = True
                if not is_method_section:
                    continue
                for j in range(i + 1, len(tag_list)):
                    next_tag = tag_list[j]
                    if next_tag.name == 'h4':
                        if j + 1 >= len(tag_list):
                            break
                        api_name = next_tag.getText()
                        api_names.add(api_name)
                        pre_tag = tag_list[j + 1]
                        if pre_tag.name == "pre":
                            signature = pre_tag.getText()
                        else:
                            continue
                        self.apis.append(api_name)
                        api_names.add(api_name)
                        api2signature[api_name] = signature
                        if j + 2 < len(tag_list) and tag_list[j + 2].name == "div":
                            description = tag_list[j + 2].getText()
                            api2des[api_name] = description
        # print("first=" + str(len(self.apis)))
        # print("second=" + str(len(api2des)))
        for api in api_names:
            is_sensitive = False
            privacy_item = ""
            for keywords in self.sensitive_keywords:
                is_sensitive = True
                for keyword in keywords:
                    if keyword.lower() not in api.lower():
                        is_sensitive = False
                if is_sensitive:
                    privacy_item = keywords
                    break
            if is_sensitive:
                self.sensitive_apis.append((self.processing_class, api, privacy_item))
                fp = fp + 1
                continue
            tp = tp + 1
        # for api_name, description in api2des.items():
        #     is_sensitive = False
        #     privacy_item = ""
        #     for keywords in self.sensitive_keywords:
        #         is_sensitive = True
        #         for keyword in keywords:
        #             if keyword.lower() not in api_name.lower():
        #                 is_sensitive = False
        #         if is_sensitive:
        #             privacy_item = keywords
        #             break
        #     if is_sensitive:
        #         self.sensitive_apis.append((self.processing_class, api_name, description, privacy_item))
        #         fp = fp + 1
        #         continue
        #     tp = tp + 1
        return tp, fp

    def print_results(self):
        # print("--------------------------------------")
        # for api in self.apis:
        #     print(api)
        print("**************************************")
        for sensitive_api in self.sensitive_apis:
            print(sensitive_api)
        print("--------------------------------------")
        print("API SUM=" + str(len(self.apis)))
        print("Sensitive API SUM=" + str(len(self.sensitive_apis)))

    def print_to_csv(self):
        csv_name = "./api_results/" + Config.target_folder.split("\\")[-1] + ".csv"
        with open(csv_name, "w") as csv_file:
            fieldnames = ["Class", "API_Name", "Reason"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                writer.writerow(
                    {"Class": sensitive_api[0], "API_Name": sensitive_api[1], "Reason": sensitive_api[2]}
                )
