# Finance-GPT
用于金融领域的智能问答客服
# 它能做什么？
## 基础版
### 金融咨询

- 该模组可以在中国金融语境下，与用户展开关于金融话题的多轮对话，或是为用户解释金融专业的相关知识。如智能金融技术知识回答，情感分析，
- 用到的技术：RAG, 微调
- 用到的数据：爬取维基百科等，网上检索现有数据集（如情感分析），调用大模型根据材料生成问题和答案
### 金融知识检索问答

- 该模组可以基于金融新闻、研报和相关政策文件为用户提供投资建议、时事分析、政策解读。
- 用到的技术：RAG
- 用到的数据：爬取东方财富网新闻研报等文本材料
### 增加网络搜索：可以调用浏览器搜索API来生成回答
### 网页化demo部署展示
## 用到的技术（InternLM训练营有教程）
### RAG（Retrieval Augmented Generation，增强检索生成）
先将金融知识等材料文本向量化处理存储至本地作为数据库，用户进行提问时，将问题向量化，然后算相似度找到最接近的文本材料作为Prompt（提示）来让基础大模型对问题和材料做一个总结性的回答。

- 优点：回答效果较好，准确。
- 缺点：每篇材料不能过长，与基础模型的输入最大token限制有关，可以将材料按内容分块存储。
### Lora微调
**LORA**是一种低资源微调大模型方法，使用LORA，训练参数仅为整体参数的万分之一、GPU显存使用量减少2/3且不会引入额外的推理耗时。基础模型参数锁住不变，增加新参数，使用数据进行微调。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/40736923/1713164742659-5e3724ae-10a9-4c9d-8a16-f8efb3d90de6.png#averageHue=%23e08f49&clientId=uea7a41a6-84ef-4&from=paste&height=188&id=uffa375c3&originHeight=376&originWidth=405&originalType=binary&ratio=2&rotation=0&showTitle=false&size=37233&status=done&style=none&taskId=u69686d65-35bf-4cdf-94e8-2378d617ca0&title=&width=202.5)
## 任务分配

- 调研整理
   - 数据集整理
      - JSON问答数据集进行微调，每类问答问题尽量多
      - ![截屏2024-04-15 16.03.16.png](https://cdn.nlark.com/yuque/0/2024/png/40736923/1713168201694-6a491717-172a-4ae8-bbdb-da9dd7d2c10e.png#averageHue=%23e9e2d7&clientId=uea7a41a6-84ef-4&from=drop&id=t7KYi&originHeight=1336&originWidth=2228&originalType=binary&ratio=2&rotation=0&showTitle=false&size=1776543&status=done&style=none&taskId=uc59c2f2f-3514-492c-b0c9-48796fea785&title=)
         - huggingface高质量金融类数据集进行翻译
         - github等网站
         - 东方财富等网站收集数据，使用大模型进行整理问答对。
      - 文档类材料数据集用于RAG，需要准确度比较高的数据，如金融专业知识。
         - ![截屏2024-04-15 16.10.09.png](https://cdn.nlark.com/yuque/0/2024/png/40736923/1713168620145-18d2a8aa-0c76-472a-ae0f-972d3ced1e99.png#averageHue=%23eee7dc&clientId=uea7a41a6-84ef-4&from=drop&id=u9622b69f&originHeight=1256&originWidth=2044&originalType=binary&ratio=2&rotation=0&showTitle=false&size=1717929&status=done&style=none&taskId=u06512304-ad38-4637-b29b-088dcac74c9&title=)
         - 东方财富
         - 维基百科
         - github等网站
   - 模型多卡并行微调（重要），模型量化压缩等技术的调研。
- 模型训练，部署，测试效果，随时更新。
# 进阶版功能（时间允许再做）
![image.png](https://cdn.nlark.com/yuque/0/2024/png/40736923/1713164967888-3399d8a2-5d6e-421d-9b26-69e671fd30d7.png#averageHue=%23cffa9e&clientId=uea7a41a6-84ef-4&from=paste&height=1148&id=ue9432b27&originHeight=2295&originWidth=3579&originalType=binary&ratio=2&rotation=0&showTitle=false&size=782564&status=done&style=none&taskId=u45838a2a-8f38-4561-8085-ed06020a79f&title=&width=1789.5)
## 将基础版金融助手部署到微信群（InternLM有教程）
## 支持云端多模型调用（Kimi，GPT-4等），InternLM有教程
## 调用简单的数据分析Agent，能画图。
## 增加多类数据集再微调

- 量化预测
- 欺诈识别

