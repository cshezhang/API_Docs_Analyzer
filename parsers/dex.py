import os
import csv
import lief
from util.config import Config
from util.MethodChecker import check_api, check_api_by_keywords
from util.Command import shell_command


# This parser also can process jar file if dx provided.
class DexFileParser:

    def __init__(self, dex_path):
        self.dex_name = dex_path.split("\\")[-1][: -4]
        if ".jar" in dex_path:
            source_folder = os.path.dirname(dex_path)
            file_name = os.path.basename(dex_path)[: -4]
            target_path = source_folder + "\\" + file_name + ".dex"
            source_path = dex_path
            dx_cmd = Config.dx_path + " --dex --output=" + target_path + " " + source_path
            # print(dx_cmd)
            if not os.path.exists(target_path):
                return_code, out, err = shell_command(dx_cmd)
                # print(return_code)
                if return_code == 1:
                    print(out)
                else:
                    print(err.decode())
        else:
            target_path = dex_path
        self.dex = lief.DEX.parse(target_path)
        self.classes = self.dex.classes
        self.apis = []
        self.sensitive_apis = []
        self.methods = self.dex.methods

    def run(self):
        for method in self.methods:
            clazz = method.cls
            if "javax/" in clazz.package_name or "java/" in clazz.package_name or "android/" in clazz.package_name or "org/w3c" in clazz.package_name:
                continue
            if "<init>" == method.name or "<clinit>" == method.name or "toString" == method.name or "clone" == method.name:
                continue
            if len(method.name) == 1:
                continue
            para_list = method.prototype.parameters_type
            if len(para_list) == 2:
                if para_list[0] == "Ljava/lang/String;" and para_list[1] == "Ljava/lang/String;":
                    print(method)
            self.apis.append(method.name)
            is_sensitive, privacy_item = check_api_by_keywords(method.name)
            if is_sensitive:
                self.sensitive_apis.append([method.cls.fullname, method.name, privacy_item])

    def get_all_classes(self):
        return self.classes

    def get_all_methods(self):
        return self.methods

    def print_results(self):
        print("--------------------------------------")
        for api in self.apis:
            print(api)
        print("**************************************")
        for sensitive_api in self.sensitive_apis:
            print(sensitive_api)
        print("API SUM=" + str(len(self.apis)))
        print("Sensitive API SUM=" + str(len(self.sensitive_apis)))

    def print_to_csv(self):
        if not os.path.exists("./api_results/dex/"):
            os.mkdir("./api_results/dex")
        csv_name = "./api_results/dex/" + self.dex_name + ".csv"
        with open(csv_name, "w") as csv_file:
            fieldnames = ["Class", "API_Name", "Reason"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            for sensitive_api in self.sensitive_apis:
                if check_api(sensitive_api[1]):
                    writer.writerow({
                        "Class": sensitive_api[0],
                        "API_Name": sensitive_api[1],
                        "Reason": sensitive_api[2]
                        })
