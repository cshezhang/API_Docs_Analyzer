# Java_Doc_Analyzer is used to automatically extract sensitive APIs from java-style api docs.
# Senstive API is based on the related keyword match.

import os
import csv
from bs4 import BeautifulSoup

from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_files, get_first_layer_folders
from util.MethodChecker import check_api, check_api_by_keywords


class JavaLikeDocParser:

    def __init__(self, target_folder=""):
        self.apis = set()
        self.processing_class = ""
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
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            tag_list = soup.find_all()
            c_tp, c_fp = self.get_privacy(tag_list)
            tp = tp + c_tp
            fp = fp + c_fp
        return tp, fp

    def get_privacy(self, tag_list):
        api_names = []
        api_descriptions = []
        tp = 0
        fp = 0
        for tag in tag_list:
            if tag.name == 'table' and 'class' in tag.attrs.keys() and 'jd-inheritance-table' in tag.attrs['class']:
                td_list = tag.find_all("td")
                self.processing_class = td_list[-1].getText()
                break
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            is_method_section = False
            if tag.name == 'h2':
                des_text = tag.getText()
                if "Public Methods" in des_text:
                    is_method_section = True
                if not is_method_section:
                    continue
                for j in range(i + 1, len(tag_list)):
                    next_tag = tag_list[j]
                    if next_tag.name == 'span' and 'class' in next_tag.attrs.keys() and 'sympad' in next_tag.attrs['class']:
                        if j + 1 >= len(tag_list):
                            break
                        api_name = next_tag.getText()
                        api_names.append(api_name)
                        if tag_list[j + 5].name == "div" and 'class' in tag_list[j + 5].attrs.keys() and 'jd-tagdescr' in tag_list[j + 5].attrs['class']:
                            api_description = tag_list[j + 5].getText()
                            api_descriptions.append(api_description)
                        else:
                            api_descriptions.append("")
        for i in range(len(api_names)):
            api = api_names[i]
            self.apis.add(api)
            api_description = api_descriptions[i]
            is_sensitive, privacy_item = check_api_by_keywords(api)
            if is_sensitive:
                api_description = api_description.replace("\n", " ")
                self.sensitive_apis.append((self.processing_class, api, privacy_item, api_description))
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
        if not os.path.exists(".\\api_results\\javalike"):
            os.mkdir(".\\api_results\\javalike")
        csv_name = ".\\api_results\\javalike\\" + self.api_folders[0].split("\\")[-2] + ".csv"
        with open(csv_name, "w") as csv_file:
            field_names = ["Class", "API_Name", "Privacy_Item", "Description"]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            for sensitive_api in self.sensitive_apis:
                if check_api(sensitive_api[1]):
                    writer.writerow({"Class": sensitive_api[0], "API_Name": sensitive_api[1], "Privacy_Item": sensitive_api[2], "Description": sensitive_api[3]})
