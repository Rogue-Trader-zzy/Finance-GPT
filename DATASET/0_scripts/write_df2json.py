import argparse
import sys

import pyarrow as pa
import pyarrow.parquet as pq
import json





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=u'E:\\big_model\\Download\\Dataset\\data\\sentiment.parquet',
                        help='Date of experiment')

    parser.add_argument('--output', type=str, default='target_output_file.json',
                        help='path of training data')
    args = parser.parse_args()

    df = pq.read_table(args.input).to_pandas()
    # 假设df是你的DataFrame，包含input、instruction和output列
    # 如果没有text列，先添加一个空的text列
    df['text'] = ''
    # 将DataFrame转换为字典列表
    data = df.to_dict(orient='records')

    with open('output_file.json', 'w') as f:
        f.write("[\n")
        for item in data:
            json.dump(item, f, indent=2)  # 设置缩进为2个空格，使得每个键值对占据一行
            f.write('\n')

    # 初始化一个空列表用于存储格式化后的键值对
    formatted_data = []

    # 提取每个JSON对象中的键值对并格式化
    for obj in data:
        print(obj)
        for key, value in obj.items():
            formatted_data.append(json.dumps({key: value}))
        sys.exit(1)

    # 写入格式化后的键值对到新的JSON文件
    with open(args.output, 'w') as f:
        f.write('\n'.join(formatted_data))