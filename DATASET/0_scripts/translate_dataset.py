import json
import sys

from concurrent.futures import ThreadPoolExecutor
import pyarrow as pa
import pyarrow.parquet as pq
import dashscope
import os
# import multiprocessing


# # 使用os模块获取CPU核心数
# num_cores = os.cpu_count()
# print("CPU核心数（os.cpu_count()）:", num_cores)
#
# # 使用multiprocessing模块获取CPU核心数
# num_cores = multiprocessing.cpu_count()
# print("CPU核心数（multiprocessing.cpu_count()）:", num_cores)
#
# df = pq.read_table(u'E:\\big_model\\Download\\Dataset\\data\\train-00000-of-00001-dabab110260ac909.parquet').to_pandas()
# print(df.head())
# print(df.columns)
# print("input: ", df.iloc[1,0])
# print("output: ", df.iloc[1,1])
# print("instruction: ", df.iloc[1,2])

from googletrans import Translator
#
# translator = Translator(service_urls=[
#       'translate.google.cn',
#     ])


# translator = Translator()
options = {
    "negative": "负面的",
    "neutral": "中性的",
    "positive": "正面的",
    "moderately positive": "适度正面",
    "mildly positive": "稍微正面",
    "strong positive": "强烈正面",
    "moderately negative": "适度负面",
    "mildly negative": "稍微负面",
    "strong negative": "强烈负面",
}

# 定义一个函数用于翻译文本
def translate_text(text):
    print("text: ", text)
    translator = Translator(service_urls=['translate.google.com'])
    result = translator.translate(text, src='en', dest='zh-cn')
    # try:
    #     translated = translator.translate(text, src='en', dest='zh-CN')
    #     result = translated.text
    # except Exception as e:
    #     result = text
    print("result: ", result.text)
    sys.exit(1)
    return result

def translate_entry(entry):
    translated_entry = {}
    for key, value in entry.items():
        print("value: ", value)
        if isinstance(value, str) and key == "input":
            translated_entry[key] = translate_text(value)
            print("input: ", translate_text(value))
        elif isinstance(value, str) and key == "instruction":
            problem = value.split("?")[0].strip() + "?"
            option = value.split("?")[1].strip()
            # 原始句子
            original_sentence = option
            # 将句子按照分隔符 '{}' 分割成两部分
            prefix, options_text = original_sentence.split("{")
            options_text, suffix = options_text.split("}")
            # options_text = options_text.replace("}", "")  # 去除末尾的 '}'
            print("options_text: ", options_text)

            # 将选项文本按照分隔符 '/' 分割成列表
            options_list = options_text.split("/")

            # 将原始句子中的选项用字典对应的值替换
            mapped_options = [options.get(option.strip(), "Unknown") for option in options_list]

            # 生成替换后的句子
            replaced_sentence = "{" + "/".join(mapped_options) + "}"
            option_sentence = "请从" + replaced_sentence + "中选择答案。"
            translated_entry[key] = translate_text(problem) + option_sentence
            print("instruction: ", translate_text(problem) + option_sentence)
        elif isinstance(value, str) and key == "output":
            translated_entry[key] = options.get(value)
            print("output: ", options.get(value))
        else:
            translated_entry[key] = value
        print("translated_entry: ", translated_entry)
    return translated_entry

def translate_json_multithreaded(data_chunk):
    translated_data = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(translate_entry, entry): entry for entry in data_chunk}
        for future in futures:
            try:
                translated_entry = future.result()
                translated_data.append(translated_entry)
            except Exception as e:
                print(f"An error occurred: {e}")

    return translated_data

# 用法示例：
input_file = 'C:\\Users\\zzy\\Documents\\5_FinGPT\\Finance-GPT\\DATASET\\0_scripts\\output_file_1.json'
output_file = 'C:\\Users\\zzy\\Documents\\5_FinGPT\\Finance-GPT\\DATASET\\0_scripts\\output_file\\'
# api_key = 'sk-e846980f5fd54e55bf2ed6483ae853b1'
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 按照每2000个entry划分数据
chunk_size = 10
for i in range(0, len(data), chunk_size):
    data_chunk = data[i:i + chunk_size]
    translated_chunk = translate_json_multithreaded(data_chunk)
    if i // 10 == 0:
        print(i)

    # 存储每个chunk的翻译结果
    with open(f'{output_file}output_{i // chunk_size}.json', 'w', encoding='utf-8') as f:
        json.dump(translated_chunk, f, ensure_ascii=False, indent=2)

# translated_df = df.applymap(translate_text)
# print(translated_df.head())
# translated_df.to_csv("translated_sentiment.csv", index=False)