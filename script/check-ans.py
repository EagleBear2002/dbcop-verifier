import os
import json

from sqlalchemy import true, false

def get_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
    return last_line

def check_min_violation(directory1, directory2):
    all_pass = true
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

                    if min_violation1 == min_violation2:
                        print(f"Min violation for {file} is the same: {min_violation1}")
                    else:
                        all_pass = false
                        print("Different:")
                        print(f"{file_path1} is {min_violation1}")
                        print(f"{corresponding_file_path2} is {min_violation2}")
                        print(f"Min violation for {file} is different.")

    if all_pass:
        print("\033[32mAll passed!\033[0m")

project_path = os.path.join('.')

# target log path
directory1 = os.path.join(project_path, 'results', 'results-status-cnt', 'galera_all_writes')
directory2 = os.path.join(project_path, 'results', 'results-status-cnt-improved-building-graph', 'galera_all_writes')

# run check
check_min_violation(directory1, directory2)
