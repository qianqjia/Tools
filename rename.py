#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
 @ Author     : Lichee
 @ Date       : 2024/06/04 23:44:54
 @ Description: 
'''


import os
from PIL import Image

# 定义文件夹路径和新的文件名前缀
folder_path = 'G:\Dataset\【Beyond NeRF Water】\data_real041\downsample\images'
new_name_prefix = ''

# 获取文件夹中的所有文件
file_list = os.listdir(folder_path)

# 遍历文件列表
for i, file_name in enumerate(file_list):

    if 'JPG' in file_name:

         # 构建旧文件的完整路径
        old_file_path = os.path.join(folder_path, file_name)
        
        # 打开图片文件
        img = Image.open(old_file_path)
        
        # 构建新文件名
        new_file_name = file_name.replace('raw2', 'raw1')+''

        # 构建新文件的完整路径
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # 保存图片文件并修改文件名
        img.save(new_file_path)
        
        # 关闭图片文件
        img.close()
        
        # 删除原始文件
        #os.remove(old_file_path)
        
'''

    # 检查文件扩展名是否为图片格式（这里只考虑了常见的图片格式，可以根据需要进行扩展）
    if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # 构建旧文件的完整路径
        old_file_path = os.path.join(folder_path, file_name)
        
        # 打开图片文件
        img = Image.open(old_file_path)
        
        # 构建新文件名
        new_file_name = f"{new_name_prefix}{i:03}.jpg"
        
        # 构建新文件的完整路径
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # 保存图片文件并修改文件名
        img.save(new_file_path)
        
        # 关闭图片文件
        img.close()
        
        # 删除原始文件
        os.remove(old_file_path)

        '''