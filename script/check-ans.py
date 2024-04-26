import os
import json

from sqlalchemy import true, false

def get_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
    return last_line

def check_min_violation(directory1, directory2):
    pass_cnt = 0
    fail_cnt = 0
    none_cnt = 0
    testcase_cnt = 0
    for root, dirs, files in os.walk(directory1):
        for file in files:
            if file.endswith('result_log.json'):
                file_path1 = os.path.join(root, file)
                corresponding_file_path2 = file_path1.replace(directory1, directory2)

                if os.path.isfile(corresponding_file_path2):
                    last_line1 = get_last_line(file_path1)
                    last_line2 = get_last_line(corresponding_file_path2)

                    json_data1 = json.loads(last_line1)
                    json_data2 = json.loads(last_line2)

                    min_violation1 = json_data1.get('minViolation')
                    min_violation2 = json_data2.get('minViolation')

                    testcase_cnt += 1
                    if min_violation1 == min_violation2:
                        pass_cnt += 1
                        # print(f"Min violation for {root}/{file} is the same: {min_violation1}")
                    elif min_violation2 == None:
                        none_cnt += 1
                    else:
                        fail_cnt += 1
                        # print("Different:")
                        # print(f"{file_path1} is {min_violation1}")
                        # print(f"{corresponding_file_path2} is {min_violation2}")
                        # print(f"Min violation for {file} is different.")

    if fail_cnt == testcase_cnt:
        print(f"\033[32m{pass_cnt} testcases All passed!\033[0m")
    else:
        print(f"\033[32m{pass_cnt} testcases passed!\033[0m")
        print(f"\033[91m{fail_cnt} testcases failed!\033[0m")
        print(f"\033[33m{none_cnt} testcases have no output for TLE!\033[0m")


project_path = os.path.join('.')

# target log path
directory1 = os.path.join(project_path, 'results', 'results-status-cnt')
directory2 = os.path.join(project_path, 'results', 'smc-algorithm')

# run check
check_min_violation(directory1, directory2)
