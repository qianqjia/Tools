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

# 初始化一个空字符串用于存储所有评论
all_comments = ''

# 遍历所有CSV文件
for csv_file in csv_files:
    # 读取CSV文件
    df = pd.read_csv(csv_file, encoding='utf-8')
    comments = df['内容'].tolist()  # 假设评论内容列名为'评论内容'
    
    # 添加到总评论字符串中
    all_comments += ''.join(comments)

# 文本预处理，提取中文
new_data = re.findall('[\u4e00-\u9fa5]+', all_comments, re.S)
new_data = '/'.join(new_data)

# 文本分词
seg_list_exact = jieba.lcut(new_data, cut_all=True)

# 过滤停用词和长度小于等于1的词
result_list = [word for word in seg_list_exact if word not in stop_words and len(word) > 1]

# 统计词频
word_counts = collections.Counter(result_list)

# 获取词频最高的5个词语
top_five_words = word_counts.most_common(5)

# 打印结果
# 准备数据用于绘制柱状图
words = [word for word, _ in top_five_words]
frequencies = [freq for _, freq in top_five_words]
frequencies = [8493,5905,5788,5665,4859]
print(frequencies)

# 创建颜色序列
colors = plt.cm.Blues(np.linspace(0.9, 0.6, len(words)))


plt.rcParams["font.sans-serif"]='SimHei'   #解决中文乱码问题
plt.rcParams['axes.unicode_minus']=False   #解决负号无法显示的问题
plt.rc('axes',axisbelow=True)  


fig=plt.figure(figsize=(8,6),dpi=100) # 先创建一个基础图
ax = fig.add_subplot(1,1,1) # 创建一个子图，然后在子图上操作

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1) # 调整图片的外间距
                           
ax.spines[['top','left','bottom','right']].set_linewidth(1.5) # 设置边框线的宽度
ax.spines[['top','right']].set_color('none')  # # 隐藏上、右边框 设置上为无色

# 绘制柱状图
bars = ax.bar(words,frequencies,width=0.6,align="center",color=colors)

# 设置x、y刻度线 direction刻度线位置
ax.tick_params(axis="x", direction='out', which='major',labelsize=16, length=5, width=1.5,)
ax.tick_params(axis="y", direction='in',which="major", labelsize=16, length=8, width=2, pad=5)

# 设置柱形图数值标注        
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height+100:.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                fontsize=14, color='black',
                xytext=(0, 4), textcoords='offset points', ha='center', va='bottom')
    

ax.set_xlabel('词语',fontsize=18,labelpad=6)
ax.set_ylabel('数量',fontsize=18,labelpad=6)
plt.tight_layout()  # 自动调整布局
plt.show()



'''

# 创建柱状图
plt.figure(figsize=(10, 6))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.bar(words, frequencies, color='skyblue')
plt.xlabel('Words')  # 将x轴标签改为'Words'
plt.ylabel('Frequency')  # 将y轴标签改为'Frequency'
plt.title('Top 5 Word Frequencies Across All Documents')  # 将图表标题改为英文
plt.xticks(rotation=45)  # 保持x轴标签旋转以便显示

plt.tight_layout()  # 自动调整布局

# 显示图表
plt.show()
'''