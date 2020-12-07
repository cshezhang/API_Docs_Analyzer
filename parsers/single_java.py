# Java_Doc_Analyzer is used to automatically extract sensitive APIs from java-style api docs.
# Senstive API is based on the related keyword match.

import os
import csv
from bs4 import BeautifulSoup

from util.log import logger
from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_files, get_first_layer_folders
from util.MethodChecker import filter_api, check_api_by_class


class SingleJavaDocParser:

    def __init__(self, target_folder=""):
        self.processing_class = ""
        self.apis = []
        self.sensitive_keywords = set()
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
            # We should consider the full class name here.
            # logger.info("Processing Class=" + self.processing_class)
            try:
                soup = BeautifulSoup(open(file, encoding="gb18030"), features='html.parser')
            except Exception:
                soup = BeautifulSoup(open(file, encoding="utf-8"), features='html.parser')
            tag_list = soup.find_all()
            c_tp, c_fp = self.get_privacy(tag_list)
            tp = tp + c_tp
            fp = fp + c_fp
        return tp, fp

    def get_privacy(self, tag_list):
        api_names = []
        api_descriptions = []
        api2signature = {}
        tp = 0
        fp = 0
        pkg_name = ""
        classname = ""
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            if tag.name == 'h2':
                pkg_name = tag_list[i - 1].getText()
                classname = tag.getText().split(" ")[-1]
            is_method_section = False
            if tag.name == 'h3':
                des_text = tag.getText()
                if "Public Member Functions" in des_text or "Method Detail" in des_text or "方法详细资料" in des_text or "メソッドの詳細" in des_text:
                    is_method_section = True
                if not is_method_section:
                    continue
                for j in range(i + 1, len(tag_list)):
                    next_tag = tag_list[j]
                    if next_tag.name == 'h4':
                        if j + 1 >= len(tag_list):
                            break
                        api_name = next_tag.getText()
                        pre_tag = tag_list[j + 1]
                        if pre_tag.name == "pre":
                            signature = pre_tag.getText()
                        else:
                            continue
                        api_names.append(api_name)
                        self.apis.append(api_name)
                        api2signature[api_name] = signature
                        if j + 2 < len(tag_list) and tag_list[j + 2].name == "div":
                            description = tag_list[j + 2].getText()
                            # print("*******************")
                            # print(api_name)
                            # print(description)
                            # print("===================")
                            api_descriptions.append(description)
                        else:
                            api_descriptions.append("")

        for i in range(0, len(api_names)):
            api_name = api_names[i]
            api_description = api_descriptions[i]
            is_sensitive, privacy_item = check_api_by_class(classname, api_name)
            if is_sensitive:
                api_description = api_description.replace("\n", " ")
                self.sensitive_apis.append((pkg_name + "." + classname, api_name, privacy_item, api_description))
                if pkg_name == "":
                    logger.error(classname)
                fp = fp + 1
                continue
            tp = tp + 1
        return tp, fp

    def print_results(self):
        print("API SUM=" + str(len(self.apis)) + "  Sensitive API SUM=" + str(len(self.sensitive_apis)))

    def print_to_csv(self):
        target_folder = ".\\api_results"
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        csv_path = target_folder + os.sep + self.api_folders[0].split("\\")[-2] + ".csv"
        csv_file = open(csv_path, "w", encoding="utf-8")
        field_names = ["Class", "API_Name", "Privacy_Item", "Description"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        # writer.writeheader()
        sensitive_cnt = 0
        for sensitive_api in self.sensitive_apis:
            if filter_api(sensitive_api[1]):
                writer.writerow(
                    {"Class": sensitive_api[0], "API_Name": sensitive_api[1], "Privacy_Item": sensitive_api[2],
                     "Description": sensitive_api[3]})
                sensitive_cnt = sensitive_cnt + 1
        print("Sensitive API SUM=" + str(sensitive_cnt))
        csv_file.close()
