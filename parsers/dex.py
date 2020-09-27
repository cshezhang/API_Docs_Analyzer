import os
import lief
from util.config import Config
from res.traverseSensitiveSources import sensitive_keywords
from util.Command import shell_command


# This parser also can process jar file if dx provided.
class DexFileParser:

    def __init__(self, dex_path):
        print(dex_path)
        if ".jar" in dex_path:
            source_folder = os.path.dirname(dex_path)
            file_name = os.path.basename(dex_path)[ : -4]
            target_path = source_folder + "\\" + file_name + ".dex"
            source_path = dex_path
            dx_cmd = Config.dx_path + " --dex --output=" + target_path + " " + source_path
            print(dx_cmd)
            return_code, out, err = shell_command(dx_cmd)
            print(return_code)
            print(out)
            print(str(err))
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
            self.apis.append(method.name)
            for keywords in sensitive_keywords:
                tag = True
                for keyword in keywords:
                    if keyword not in method.name:
                        tag = False
                if tag:
                    self.sensitive_apis.append(method.name)
                    break

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
        print("--------------------------------------")
        print("API SUM=" + str(len(self.apis)))
        print("Sensitive API SUM=" + str(len(self.sensitive_apis)))
