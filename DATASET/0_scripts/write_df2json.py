import argparse
import sys

import pyarrow as pa
import pyarrow.parquet as pq
import json





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=u'E:\\big_model\\Download\\Dataset\\data\\finred.parquet',
                        help='Date of experiment')

    parser.add_argument('--output', type=str, default='finred.json',
                        help='path of training data')
    parser.add_argument('--format_output', type=str, default='formatted_finred.json',
                        help='path of training data')
    args = parser.parse_args()

    df = pq.read_table(args.input).to_pandas()
    # 假设df是你的DataFrame，包含input、instruction和output列
    # 如果没有text列，先添加一个空的text列
    df['text'] = ''
    # 将DataFrame转换为字典列表
    data = df.to_dict(orient='records')

    with open(args.output, 'w') as f:
        for item in data:
            json.dump(item, f, indent=2)  # 设置缩进为2个空格，使得每个键值对占据一行
            f.write(',\n')

    with open(args.output, "r") as handle:
        with open(args.format_output, "w") as writer:
            writer.write("[\n")
            for line in handle.readlines():
                writer.write("  " + line)
            writer.write("]\n")