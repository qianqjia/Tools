import sqlite3
import numpy as np

# 连接COLMAP的数据库
conn = sqlite3.connect('G:/Dataset/jqq/underwater/starfish/database.db')

cursor = conn.cursor()

# 查询2D点信息
cursor.execute("SELECT images.Name, keypoints.X, keypoints.Y FROM keypoints JOIN images ON keypoints.Image_ID = images.Image_ID")

# 获取所有2D点的信息
keypoints_info = cursor.fetchall()

# 打印2D点信息
for image_name, x, y in keypoints_info:
    print(f"Image: {image_name}, Keypoint: ({x}, {y})")

# 关闭数据库连接
conn.close()