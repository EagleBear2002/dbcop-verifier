import os
import re
import csv


def parse_massif_file(file_path):
    max_memory = 0
    input_file = ''

    with open(file_path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith('cmd:'):
                input_file = re.search(r'\/excutions\/(.*?\/hist-\d+)', line).group(1)

            if line.startswith('mem_heap_B='):
                mem_heap = int(line.split('=')[1])

            if line.startswith('mem_heap_extra_B='):
                mem_heap_extra = int(line.split('=')[1])

            if line.startswith('mem_stacks_B='):
                mem_stacks = int(line.split('=')[1])

            if line.startswith('heap_tree='):
                total_memory = mem_heap + mem_heap_extra + mem_stacks
                max_memory = max(max_memory, total_memory)

    return input_file, max_memory


def write_to_csv(result_file, input_file, max_memory):
    file_exists = os.path.exists(result_file)

    with open(result_file, 'a', newline='') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(['testcase', 'max-mem in bytes'])

        writer.writerow([input_file, max_memory])


def process_massif_files(directory):
    result_file = os.path.join(directory, 'mem-results/mem-results-smc.csv')

    # Collect all massif.out files in the directory
    massif_files = [f for f in os.listdir(directory) if f.startswith('massif.out.')]

    for file in massif_files:
        file_path = os.path.join(directory, file)
        input_file, max_memory = parse_massif_file(file_path)
        write_to_csv(result_file, input_file, max_memory)


# Specify the directory containing massif.out files
directory = './'

# Process the massif files and generate the results
process_massif_files(directory)
