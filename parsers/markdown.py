# Java_Doc_Analyzer is used to automatically extract sensitive APIs from java-style api docs.
# Senstive API is based on the related keyword match.

import io
import sys
import csv
from bs4 import BeautifulSoup

from util.log import logger
from util.config import Config
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_all_files, get_first_layer_files


class MarkdownDocParser:

    def __init__(self):
        self.processing_class = ""
        self.sensitive_keywords = set()
        self.sensitive_results = set()
        self.api_cnt = 0

    def run(self):
        get_sensitive_keywords()
        print(self.sensitive_keywords)
        sum_items = 0
        sum_tp = 0
        sum_fp = 0
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        api_folders = get_first_layer_files(Config.target_folder)
        for api_folder in api_folders:
            logger.info("Processing Folder:" + str(api_folder))
            (items, tp, fp) = self.processAPI(api_folder)
            sum_items = sum_items + items
            sum_tp = sum_tp + tp
            sum_fp = sum_fp + fp
        # print("SUM_ITEMS=" + str(sum_items))
        # print("SUM_TP=" + str(sum_tp))
        # print("SUM_FP=" + str(sum_fp))
        print("-----Sensitive Results-----")
        # for sensitive_result in sensitive_results:
        #     print(sensitive_result)
        print("APIs Count=" + str(self.api_cnt))
        print("Sensitive APIs Count=" + str(len(self.sensitive_results)))

    def get_privacy(self, tag_list):
        api_names = []
        api2des = {}
        api2signature = {}
        tp = 0
        fp = 0
        api_cnt = 0
        # for i in range(0, len(tag_list)):
        #     if tag_list[i].name == "code":
        #         print(tag_list[i].getText())
        for i in range(0, len(tag_list)):
            tag = tag_list[i]  # tag is a table class used to parse method.
            is_method_section = False
            if tag.name == 'h2':
                des_text = tag.getText()
                if "Method descriptions" in des_text:
                    is_method_section = True
                if not is_method_section:
                    continue
                for j in range(i + 1, len(tag_list)):
                    next_tag = tag_list[j]
                    if next_tag.name == 'h3':
                        if j + 1 >= len(tag_list):
                            break
                        api_name = next_tag.getText()
                        api_cnt = api_cnt + 1
                        print(api_name + "  " + str(api_cnt))
                        api_names.append(api_name)
                        # pre_tag = tag_list[j + 1]
                        # if pre_tag.name == "pre":
                        #     signature = pre_tag.getText()
                        # else:
                        #     continue
                        # api_names.append(api_name)
                        # api2signature[api_name] = signature
                        if j + 2 < len(tag_list) and tag_list[j + 2].name == "code":
                            signature = tag_list[j + 2].getText()
                            # print(signature)
                            api2signature[api_name] = signature
                        if j + 3 < len(tag_list) and tag_list[j + 3].name == "p":
                            description = tag_list[j + 3].getText()
                            # print(description)
                            api2des[api_name] = description
                        else:
                            if j + 4 < len(tag_list) and tag_list[j + 4].name == "p":
                                description = tag_list[j + 4].getText()
                                print(description)
                                api2des[api_name] = description
                            else:
                                api2des[api_name] = "No Description."
        num_sensitive_apis = 0
        for api_name in api_names:
            is_sensitive = False
            # print(api_name)
            # print(api2signature[api_name])
            # print(api2des[api_name])
            for keywords in self.sensitive_keywords:
                is_sensitive = True
                # print("!!!=" + str(type(description)) + "  " + api_name)
                # if keyword in description.lower() or keyword in api_name.lower():
                for keyword in keywords:  # 一个隐私项可能有多个keyword，比如Device_ID
                    if keyword not in api_name:
                        is_sensitive = False
                if is_sensitive:
                    break
                # if keyword in api_name.lower():
                #     is_sensitive = True
                #     break
                '''and (api_name.startswith("get") or api_name.startswith("set") or api_name.startswith("add")) and 
                not api_name.endswith("Required") and not api_name.endswith("Status") and not api_name.endswith(
                "Requirements") '''
            if is_sensitive:
                self.sensitive_results.add((self.processing_class, api_name, "", keywords))
                fp = fp + 1
                continue
            tp = tp + 1
            # print(reason)
            # print("-----------------------Description-------------------------")
            # print(description)
        # global api_cnt
        # api_cnt = len(api_names)
        return (num_sensitive_apis, tp, fp, api_cnt)

    def process_api(self, folder):
        sum_sensitive_apis = 0
        tp = 0
        fp = 0
        files_list = get_all_files(folder)
        sum = 0
        for i in range(0, len(files_list)):
            file = files_list[i]
            # logger.info("Processing File=" + str(file))
            self.processing_class = file.split("\\")[-1].split(" ")[0]
            # logger.info("Processing Class=" + processing_class)
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            tag_list = soup.find_all()
            # print("tag list len=" + str(len(tag_list)))
            (num_sensitive_apis, c_tp, c_fp, ac) = self.get_privacy(tag_list)
            sum_sensitive_apis = sum_sensitive_apis + num_sensitive_apis
            tp = tp + c_tp
            fp = fp + c_fp
            sum = sum + ac
        print("Sum_Sensitive_APIs=" + str(sum_sensitive_apis))
        print("TP=" + str(tp))
        print("FP=" + str(fp))
        print("SUM=" + str(sum))
        return (sum_sensitive_apis, tp, fp)

    def print_to_csv(self):
        with open("./api_results/facebook.csv", "w") as csv_file:
            fieldnames = ["Class", "API_Name", "Description"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                writer.writerow(
                    {"Class": sensitive_api[0], "API_Name": sensitive_api[1], "Description": sensitive_api[2]}
                )

