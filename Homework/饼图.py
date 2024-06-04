import pandas as pd
import matplotlib.pyplot as plt

# 定义时间转换函数
def rate_to_sentiment(rate):
    if rate >= 4:
        return '好评'
    elif rate <= 3:
        return '差评'


# 文件列表
files = ['华为.csv', '小米.csv', '苹果.csv']

# 初始化情感计数器
sentiment_counts = {'好评': 0, '差评': 0,}

# 遍历每个CSV文件
for filename in files:
    # 读取CSV文件
    df = pd.read_csv(filename, encoding='utf-8')
    
    # 将时间列转换为整数（这里假设时间是整数形式，如果是小数则应转换为float）
    df['时间'] = pd.to_numeric(df['时间'], errors='coerce')  # errors='coerce'会将无法转换的值设为NaN
    
    # 筛选出有效的时间（即非NaN值）
    valid_ratings = df['时间'].dropna()
    
    # 应用时间转换函数并统计
    sentiments = valid_ratings.apply(rate_to_sentiment)
    for sentiment in sentiments:
        sentiment_counts[sentiment] += 1

# 绘制扇形图
labels = sentiment_counts.keys()
sizes = sentiment_counts.values()

plt.figure(figsize=(4, 4))
plt.rcParams["font.sans-serif"]='SimHei'   #解决中文乱码问题
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Evaluation and distribution of mobile phone users of different brands')
plt.show()