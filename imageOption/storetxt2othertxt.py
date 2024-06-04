# 从一个.txt文件读取并保存到另一个.txt文件中
import os
import numpy as np

path1 = 'G:/Dataset/jqq/underwater/starfish/images.txt'
path2 = 'G:/Dataset/jqq/underwater/starfish/output_file.txt'

# 读取相机外参文件
with open(path1, 'r') as f_in, open(path2, 'w') as f_out:
    for num,line in enumerate(f_in):
        if num<4:
            f_out.write(line)
        else:
            if num%2!=0:
                continue
            else:
                f_out.write(line)
