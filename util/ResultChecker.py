import os
from util.traverseFolder import get_first_layer_files, get_first_layer_folders


def process_results():
    result_folders = get_first_layer_folders("." + os.sep + "api_results")
    csv_cnt = 0
    csv_file_cnt = 0
    for res_folder in result_folders:
        csv_files = get_first_layer_files(res_folder, html=False)
        csv_file_cnt += len(csv_files)
        api_sum = 0
        for csv_file in csv_files:
            csv = open(csv_file, "r", encoding="utf-8")
            # print(csv_file)
            lines = csv.readlines()
            csv_name = csv_file.split(os.sep)[-1][:-4]
            sum_cnt = 0
            general_cnt = 0
            for line in lines:
                if "," in line:
                    sum_cnt = sum_cnt + 1
                if "logevent" in line or "GeneralLogEvent" in line or "trackEvent" in line or \
                        "GeneralUserProperty" in line:
                    general_cnt = general_cnt + 1
            api_sum += sum_cnt
            if sum_cnt >= 0:
                if general_cnt >= 0:
                    csv_cnt = csv_cnt + 1
                    # print("CSV_Name=" + csv_name + ", Privacy API=" + str(sum_cnt) + ", General API=" + str(general_cnt))
                    # print(csv_name + "," + str(sum_cnt) + "," + str(general_cnt))
                    # loss = loss + (sum_cnt - general_cnt) / sum_cnt
        if api_sum == 0:
            print("!!!=" + res_folder)
    print("CSV File Count=" + str(csv_file_cnt))