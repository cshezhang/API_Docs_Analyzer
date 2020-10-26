# Silver_Java_Doc_Analyzer is used to automatically extract sensitive APIs from java-style api docs.
# Senstive API is based on the related keyword match.

import os
import csv
from bs4 import BeautifulSoup

from util.log import logger
from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_files, get_first_layer_folders
from util.MethodChecker import check_api_by_class, filter_api


class SilverJavaDocParser:

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
        self.processing_class = self.processing_class[5:-5]
        self.processing_class = self.processing_class.replace("_1_1", ".")
        class_info = ""
        tag = False
        for ch in self.processing_class:
            if tag:
                class_info = class_info + ch.upper()
                tag = False
            else:
                if ch != "_":
                    class_info = class_info + ch
                else:
                    tag = True
        class_info = class_info.strip()
        classname = class_info.split(".")[-1]
        pkg_name = class_info[:-(len(classname) + 1)]
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            # if "Class Reference" in tag.getText() and tag.name == "title":
            #     print(tag.getText().split(":")[1].strip().split(" ")[0] + "__" + tag.name)
            #     pkg_name = tag_list[i - 1].getText()
            #     classname = tag.getText().split(" ")[-1]
            is_method_section = False
            if tag.name == 'h2':
                des_text = tag.getText()
                if "Member Function Documentation" in des_text:
                    is_method_section = True
                if not is_method_section:
                    continue
                for j in range(i + 1, len(tag_list)):
                    next_tag = tag_list[j]
                    if next_tag.name == "td" and "class" in next_tag.attrs.keys() and "memname" in next_tag.attrs["class"]:
                        # print(next_tag.getText())
                        api_name = str(next_tag.getText()).strip().split(" ")[-1]
                        if "." in api_name:
                            api_name = api_name.split(".")[-1]
                        # print(api_name)
                        # if pre_tag.name == "pre":
                        #     signature = pre_tag.getText()
                        # else:
                        #     continue
                        api_names.append(api_name)
                        self.apis.append(api_name)
                        # api2signature[api_name] = signature
                        # if j + 2 < len(tag_list) and tag_list[j + 2].name == "div":
                        #     description = tag_list[j + 2].getText()
                        #     # print("*******************")
                        #     # print(api_name)
                        #     # print(description)
                        #     # print("===================")
                        #     api_descriptions.append(description)
                        # else:
                        #     api_descriptions.append("")

        for i in range(0, len(api_names)):
            api_name = api_names[i]
            # api_description = api_descriptions[i]
            is_sensitive, privacy_item = check_api_by_class(classname, api_name)
            if is_sensitive:
                # api_description = api_description.replace("\n", " ")
                self.sensitive_apis.append((pkg_name + "." + classname, api_name, privacy_item))
                # self.sensitive_apis.append((pkg_name + "." + classname, api_name, privacy_item, api_description))
                if pkg_name == "":
                    logger.error(classname + " no Class!")
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
        if not os.path.exists(".\\api_results\\silverjava"):
            os.mkdir(".\\api_results\\silverjava")
        csv_name = self.api_folders[0].split("\\")[-2]
        with open("./api_results/silverjava/" + csv_name + ".csv", "w") as csv_file:
            fieldnames = ["Class", "API_Name", "Reason"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                if filter_api(sensitive_api[1]):
                    writer.writerow(
                        {"Class": str(sensitive_api[0]), "API_Name": str(sensitive_api[1]), "Reason": str(sensitive_api[2])}
                    )
