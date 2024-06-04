import jieba
import collections
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('华为.csv', encoding='utf-8') as f:
    data = f.read()

# 文本预处理  去除一些无用的字符   只提取出中文出来
new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
new_data = "/".join(new_data)

# 文本分词
seg_list_exact = jieba.lcut(new_data, cut_all=True)

result_list = []

with open('stop_words.txt', encoding='utf-8') as f:
    lines = f.readlines()
    stop_words = set()
    for line in lines:
        # 根据分隔符分割每一行的字符串，这里假设分隔符是逗号 ","
        words = line.strip().split(', ')
        # 将分割后的单词列表转换为集合，以避免重复
        stop_words.update(words)


for word in seg_list_exact:
    # 设置停用词并去除单个词
    if word not in stop_words and len(word) > 1:
        result_list.append(word)
print(result_list)

# 筛选后统计
word_counts = collections.Counter(result_list)

# 绘制词云
my_cloud = WordCloud(
    background_color='white',  # 设置背景颜色  默认是black
    width=800, height=550,
    font_path='simhei.ttf',   # 设置字体  显示中文
    max_font_size=130,        # 设置字体最大值
    min_font_size=12,         # 设置子图最小值
    random_state=80,           # 设置随机生成状态，即多少种配色方案
    colormap='tab20b'          # 设置配色方案
).generate_from_frequencies(word_counts)

# 显示生成的词云图片
plt.imshow(my_cloud, interpolation='bilinear')
# 显示设置词云图中无坐标轴
plt.axis('off')
plt.show()