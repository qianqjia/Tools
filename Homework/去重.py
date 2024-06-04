import jieba
import collections
import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

# CSV文件列表
csv_files = ['华为.csv', '小米.csv', '苹果.csv']
stop_words_file = 'stop_words.txt'


# 加载停用词，这里假设停用词是以英文逗号 ',' 分隔的，并可能存在前后空格
with open(stop_words_file, encoding='utf-8') as f:
    stop_words_content = f.read().strip()  # 读取整个文件内容并去除首尾空白
stop_words = set(word.strip() for word in stop_words_content.split(','))  # 分割字符串，同时去除每个词的首尾空白，然后形成集合


# 初始化一个空列表用于存储所有评论
all_comments = []

# 遍历所有CSV文件
for csv_file in csv_files:
    # 读取CSV文件
    df = pd.read_csv(csv_file, encoding='utf-8')
    comments = df['内容'].tolist()  # 假设评论内容列名为'评论内容'
    print(len(comments))
    
    # 将每个文件的评论添加到all_comments列表中
    all_comments.extend(comments)

print(len(all_comments))
# 去除重复的评论
all_comments = list(collections.OrderedDict.fromkeys(all_comments))

# 打印去重后的评论数量
print(len(all_comments))


# 如果需要，可以在这里添加处理all_comments的代码，例如生成词云等
