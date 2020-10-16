import os
import lief
from util.config import Config
from res.traverseSensitiveSources import sensitive_keywords
from util.Command import shell_command
from util.log import logger


def __init__(self, dex_path):
    self.dex_name = dex_path.split("\\")[-1][: -4]
    if ".jar" in dex_path:
        source_folder = os.path.dirname(dex_path)
        file_name = os.path.basename(dex_path)[: -4]
        target_path = source_folder + "\\" + file_name + ".dex"
        source_path = dex_path
        dx_cmd = Config.dx_path + " --dex --output=" + target_path + " " + source_path
        # print(dx_cmd)
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
        for keywords in sensitive_keywords:
            tag = True
            for keyword in keywords:
                if keyword.lower() not in method.name.lower():
                    tag = False
            if tag:
                privacy_item = ""
                for keyword in keywords:
                    privacy_item = privacy_item + keyword + "_"
                privacy_item = privacy_item[: -1]
                self.sensitive_apis.append([method.cls.fullname, method.name, privacy_item])
                break


def get_all_classes(self):
    return self.classes


def get_all_methods(self):
    return self.methods


def print_results(self):
    # logger.info("--------------------------------------")
    # for api in self.apis:
    #     logger.info(api)
    logger.info("**************************************")
    for sensitive_api in self.sensitive_apis:
        logger.info(sensitive_api)
    logger.info("API SUM=" + str(len(self.apis)))
    logger.info("Sensitive API SUM=" + str(len(self.sensitive_apis)))
