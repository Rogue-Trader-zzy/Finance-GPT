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
import requests
import json


# def translate_text(text, api_key):
#     # 在此调用大模型的API进行翻译，注意处理token限制
#     # 请提供大模型调用的API示例代码
#     messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
#                 {'role': 'user', 'content': "帮我翻译为中文：" + text}]
#
#     response = dashscope.Generation.call(
#         dashscope.Generation.Models.qwen_turbo,
#         messages=messages,
#         api_key=api_key,
#         result_format='message',  # set the result to be "message" format.
#     )
#     #
#     # if response.status_code == HTTPStatus.OK:
#     #     # print(response['output']['choices'][0]['message']['content'])
#     # else:
#     #     print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
#     #         response.request_id, response.status_code,
#     #         response.code, response.message
#     #     ))
#
#     # 替换上面的示例代码，使用实际的大模型调用代码
#     # translated_text = f"Translated: {translated_text}"  # 这里仅作为示例，替换为实际翻译的结果
#     return response['output']['choices'][0]['message']['content']
def translate_text(text):
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": "请帮我把下面英文句子翻译成中文，回答中直接给出英文翻译！{" + text + "}"}
    response = requests.post(url='http://127.0.0.1:6006/', headers=headers, data=json.dumps(data))
    print("response: ", response.json()['response'])
    return response.json()['response']

# 定义一个函数用于翻译文本
# def translate_text(text):
#     print("text: ", text)
#     translator = Translator(service_urls=['translate.google.com'])
#     result = translator.translate(text, src='en', dest='zh-cn')
#     # try:
#     #     translated = translator.translate(text, src='en', dest='zh-CN')
#     #     result = translated.text
#     # except Exception as e:
#     #     result = text
#     print("result: ", result.text)
#     sys.exit(1)
#     return result

def translate_entry(entry):
    translated_entry = {}
    for key, value in entry.items():
        # print("value: ", value)
        if isinstance(value, str) and key == "input":
            translated_entry[key] = translate_text(value)
            # print("input: ", translate_text(value))
        elif isinstance(value, str) and key == "instruction":
            if "news" in value:
                translated_value = "这个新闻的情绪是什么？"
            elif "tweet" in value:
                translated_value = "这个推文的情绪是什么？"
            else:
                problem = value.split("?")[0].strip() + "?"
                option = value.split("?")[1].strip()
                # 原始句子
                original_sentence = option
                # 将句子按照分隔符 '{}' 分割成两部分
                prefix, options_text = original_sentence.split("{")
                options_text, suffix = options_text.split("}")
                # options_text = options_text.replace("}", "")  # 去除末尾的 '}'
                # print("options_text: ", options_text)

                # 将选项文本按照分隔符 '/' 分割成列表
                options_list = options_text.split("/")

                # 将原始句子中的选项用字典对应的值替换
                mapped_options = [options.get(option.strip(), "Unknown") for option in options_list]

                # 生成替换后的句子
                replaced_sentence = "{" + "/".join(mapped_options) + "}"
                option_sentence = "请从" + replaced_sentence + "中选择答案。"
                translated_value = translate_text(problem) + option_sentence
                # print("instruction: ", translate_text(problem) + option_sentence)
            translated_entry[key] = translated_value
        elif isinstance(value, str) and key == "output":
            translated_entry[key] = options.get(value)
            # print("output: ", options.get(value))
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
input_file = '/home/zzy/Documents/InternLM_API/Finance-GPT/Finance-GPT/DATASET/0_scripts/sentiment/output_file_4.json'
output_file = '/home/zzy/Documents/InternLM_API/Finance-GPT/Finance-GPT/DATASET/0_scripts/output_file/'
# api_key = 'sk-e846980f5fd54e55bf2ed6483ae853b1'
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 按照每2000个entry划分数据
chunk_size = 50
for i in range(0, int(len(data)/6), chunk_size):
    data_chunk = data[i:i + chunk_size]
    translated_chunk = translate_json_multithreaded(data_chunk)
    if i // 10 == 0:
        print(i)

    # 存储每个chunk的翻译结果
    with open(f'{output_file}output_{156 + i // chunk_size}.json', 'w', encoding='utf-8') as f:
        json.dump(translated_chunk, f, ensure_ascii=False, indent=2)

# translated_df = df.applymap(translate_text)
# print(translated_df.head())
# translated_df.to_csv("translated_sentiment.csv", index=False)
