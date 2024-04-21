import json


# 读取原始JSON文件
with open('formatted_file.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 计算每个子列表的大小
num_objects = len(data)
num_files = 5
objects_per_file = num_objects // num_files
remainder = num_objects % num_files

# 分割JSON对象列表为子列表
start_index = 0
for i in range(num_files):
    end_index = start_index + objects_per_file + (1 if i < remainder else 0)
    subset = data[start_index:end_index]

    # 写入子列表到新的JSON文件
    with open(f'output_file_{i + 1}.json', 'w') as f:
        json.dump(subset, f, indent=2)

    # 更新下一个子列表的起始索引
    start_index = end_index