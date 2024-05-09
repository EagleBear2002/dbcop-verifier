import csv
import matplotlib.pyplot as plt


def plot_data(file_path, color):
    x_values = []
    y_values = []

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            testcase = row['testcase']
            max_mem = int(row['max-mem in bytes'])

            # 提取横坐标参数
            x_value = testcase.split('/')[1].split('_')[3]
            x_values.append(x_value)

            # 提取纵坐标值
            y_values.append(max_mem)

    sorted_indices = sorted(range(len(x_values)), key=lambda k: int(x_values[k]))
    x_values = [x_values[i] for i in sorted_indices]
    y_values = [y_values[i] for i in sorted_indices]

    # 绘制图形
    plt.scatter(x_values, y_values, marker='o', color=color, alpha=0.02, s=40)


plot_data('mem-results/mem-results-raw.csv', 'blue')
plot_data('mem-results/mem-results-smc.csv', 'red')

plt.xlabel('Parameter')
plt.ylabel('Max Memory (bytes)')
plt.title('Max Memory vs Parameter')

plt.savefig('mem-results/max-mem.png')
# 显示图形
plt.show()
