# APIDoc_Analyzer is used to automatically extract sensitive API from docs.
# Senstive API is based on the related keyword.

import io
import sys
from bs4 import BeautifulSoup

from util.log import logger
from res.traverseSensitiveSources import get_sensitive_keywords
from util.traverseFolder import get_first_layer_files, get_all_files


class CodeDocParser:

    def __init__(self):
        self.processing_class = ""
        self.sensitive_keywords = set()
        self.sensitive_results = set()

    def run(self):
        get_sensitive_keywords()
        print(self.sensitive_keywords)
        sum_items = 0
        sum_tp = 0
        sum_fp = 0
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        api_folders = get_first_layer_files("E:\\Lab Work\\dataset_science\\API_Docs\\Countly_API_Docs_test\\")
        sum_acs = 0
        for api_folder in api_folders:
            logger.info("Processing Folder:" + str(api_folder))
            (items, tp, fp, acs) = self.process_api(api_folder)
            sum_acs = sum_acs + acs
            sum_items = sum_items + items
            sum_tp = sum_tp + tp
            sum_fp = sum_fp + fp
        print("SUM=" + str(sum_acs))
        # print("SUM_ITEMS=" + str(sum_items))
        # print("SUM_TP=" + str(sum_tp))
        # print("SUM_FP=" + str(sum_fp))
        print("-----Sensitive Results-----")
        for sensitive_result in self.sensitive_results:
            print(sensitive_result)
        # logger.info("API Count=" + str(api_cnt))
        logger.info("Sensitive API Count=" + str(len(self.sensitive_results)))

    def get_privacy(self, tag_list):
        blacklist = ["head", "html", "path", "Throws"]
        table_list = []
        api_names = set()
        api2des = {}
        tp = 0
        fp = 0
        api_cnt = 0
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            if tag.name == 'code':
                print(tag.getText())
                print("--------------------------------")
        if True == True:
            return
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
                            # print("target=" + str(target))
                            api_name = target[: index]
                            api_names.add(api_name)
        descriptions = []
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            if 'h' in tag.name and tag.name not in blacklist:
                has_description = False
                target_api = ""
                for api_name in api_names:
                    if api_name in tag.getText():
                        # api_names.remove(api_name)
                        has_description = True
                        target_api = api_name
                        api_cnt = api_cnt + 1
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
        num_sensitive_apis = 0

        for api_name, description in api2des.items():
            is_sensitive = False
            # privacy_item = ""
            api_cnt = api_cnt + 1
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
                self.sensitive_results.add((processing_class, api_name, description, keywords))
                fp = fp + 1
                continue
            tp = tp + 1
            # print(reason)
            # print("-----------------------Description-------------------------")
            # print(description)
        return (num_sensitive_apis, tp, fp, api_cnt)

    def process_api(self, folder):
        sum_sensitive_apis = 0
        tp = 0
        fp = 0
        files_list = get_all_files(folder)
        acs = 0
        for i in range(0, len(files_list)):
            file = files_list[i]
            # logger.info("Processing File=" + str(file))
            self.processing_class = file.split("\\")[-1].split(" ")[0]
            logger.info("Processing Class=" + self.processing_class)
            soup = BeautifulSoup(open(file, encoding='utf-8'), features='html.parser')
            # tag_list includes the whole tags in a html file.
            tag_list = soup.find_all()
            # print("tag list len=" + str(len(tag_list)))
            (num_sensitive_apis, c_tp, c_fp, ac) = self.get_privacy(tag_list)
            sum_sensitive_apis = sum_sensitive_apis + num_sensitive_apis
            tp = tp + c_tp
            fp = fp + c_fp
            acs = ac + acs
        # print("Sum_Sensitive_APIs=" + str(sum_sensitive_apis))
        # print("TP=" + str(tp))
        # print("FP=" + str(fp))
        return (sum_sensitive_apis, tp, fp, acs)
