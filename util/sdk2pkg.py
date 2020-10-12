import os
import csv


def get_all_files(target_folder):
    files = []
    list_ = os.listdir(target_folder)
    for i in range(0, len(list_)):
        path = os.path.join(target_folder, list_[i])
        if os.path.isdir(path):
            files.extend(get_all_files(path))
        if os.path.isfile(path):
            files.append(path)
    return files


def calculate_common_prefix(str1, str2):
    str_len = min(len(str1), len(str2))
    for i in range(0, str_len):
        if str1[i] == str2[i]:
            continue
        else:
            return str1[: i]
    return str1[: str_len]


def main():
    target_folder = "../api_results/java/"
    files = get_all_files(target_folder)
    for file_path in files:
        pkg_names = []
        sdk_name = file_path.split("/")[-1]
        print("SDK_Name=" + str(sdk_name[: -4]))
        with open(file_path, encoding="utf-8") as file:
            csv_file = csv.reader(file)
            for row in csv_file:
                if (len(row)) == 0:
                    continue
                if "com/google" in row[0]:
                    continue
                pkg_name = row[0]
                pkg_names.append(pkg_name)
        # print(pkg_names)
        target_prefix = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        for i in range(0, len(pkg_names) - 1):
            temp_prefix = calculate_common_prefix(pkg_names[i], pkg_names[i + 1])
            if len(temp_prefix) < len(target_prefix):
                target_prefix = temp_prefix
        if "/" in target_prefix:
            target_prefix = target_prefix.replace("/", ".")
        if target_prefix.startswith("L") and len(target_prefix) > 1:
            target_prefix = target_prefix[1 :]
        if target_prefix.endswith(".") and len(target_prefix) > 1:
            target_prefix = target_prefix[: -1]
        print("Target Prefix=" + str(target_prefix))
        print("-------------------------------------------")


if __name__ == "__main__":
    main()
