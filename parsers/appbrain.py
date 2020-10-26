# AppBrain_Doc_Analyzer is used to automatically extract sensitive APIs from java-style api docs.
# Senstive API is based on the related keyword match.

import os
import csv
from bs4 import BeautifulSoup

from util.traverseFolder import get_first_layer_files, get_first_layer_folders
from util.MethodChecker import filter_api, check_api_by_class


class AppbrainDocParser:

    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.processing_class = ""
        self.sensitive_keywords = set()
        self.apis = []
        self.sensitive_apis = []

    def run(self):
        # print(self.sensitive_keywords)
        sum_tp = 0
        sum_fp = 0
        api_folders = get_first_layer_folders(self.target_folder)
        for api_folder in api_folders:
            # logger.info("Processing Folder:" + str(api_folder))
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
            # logger.info("Processing Class=" + self.processing_class)
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            tag_list = soup.find_all()
            c_tp, c_fp = self.get_privacy(tag_list)
            tp = tp + c_tp
            fp = fp + c_fp
        return tp, fp

    def get_privacy(self, tag_list):
        api_names = set()
        # api2des = {}
        api2signature = {}
        tp = 0
        fp = 0
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            is_method_section = False
            if tag.name == 'h2':
                # print(tag.getText())
                des_text = tag.getText()
                if "Methods" in des_text:
                    is_method_section = True
                if not is_method_section:
                    continue
                for j in range(i + 1, len(tag_list)):
                    next_tag = tag_list[j]
                    if next_tag.name == "dl" and "class" in next_tag.attrs.keys() and "method" in next_tag.attrs["class"]:
                        if j + 1 >= len(tag_list):
                            break
                        signature = tag_list[j + 1]["id"]
                        api_name = signature.split(".")[-1]
                        api_name = api_name[ : api_name.rfind("(")]
                        api_names.add(api_name)
                        self.apis.append(api_name)
                        api2signature[api_name] = signature
                        # if j + 2 < len(tag_list) and tag_list[j + 2].name == "div":
                        #     description = tag_list[j + 2].getText()
                        #     api2des[api_name] = description
        # print("first=" + str(len(self.apis)))
        # print("second=" + str(len(api2des)))
        for api in api_names:
            is_sensitive, privacy_item = check_api_by_class(self.processing_class, api)
            if is_sensitive:
                self.sensitive_apis.append((self.processing_class, api, privacy_item))
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
        if not os.path.exists(".\\api_results\\appbrain"):
            os.mkdir(".\\api_results\\appbrain")
        sensitive_cnt = 0
        with open(".\\api_results\\appbrain\\appbrain.csv", "w") as csv_file:
            fieldnames = ["Class", "API_Name", "Description"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                if filter_api(sensitive_api[1]):
                    writer.writerow({"Class": sensitive_api[0], "API_Name": sensitive_api[1], "Description": sensitive_api[2]})
                    sensitive_cnt = sensitive_cnt + 1
        print("Sensitive API SUM=" + str(sensitive_cnt))