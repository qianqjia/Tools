
'''
    PSNR:常见的PSNR范围通常在20到50之间，数值越高表示图像质量越好，表示图像的质量与原始图像的相似度越高
    MS-SSIM:的值范围在0到1之间，数值越接近1表示重建图像与原始图像的相似度越高，图像质量越好
'''

import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ski_ssim
import datetime


# 设置文件夹路径
gt_folder = 'G:/Experments/0509_stuff_darkcolmap_enhanceimage/train/ours_30000/gt/'
render_folder = 'G:/Experments/0428_stuff/train/ours_30000/renders/'

# 获取文件夹中的所有图片并匹配
img_files_gt = [f for f in os.listdir(gt_folder) if os.path.isfile(os.path.join(gt_folder, f))]
img_files_render = [f for f in os.listdir(render_folder) if os.path.isfile(os.path.join(render_folder, f))]

# 确保图片数量一致
min_length = min(len(img_files_gt), len(img_files_render))

# 初始化存储结果的列表
psnr_values = []
ssim_values = []

# 计算每对图片的PSNR和SSIM值
for i in range(min_length):
    img_gt = cv2.imread(os.path.join(gt_folder, img_files_gt[i]))
    img_render = cv2.imread(os.path.join(render_folder, img_files_render[i]))
    
    # 确保图片已正确读取
    if img_gt is not None and img_render is not None:
        psnr_value = psnr(img_gt,img_render,data_range=255)
        ssim_value = ski_ssim(img_gt,img_render,data_range=255,multichannel=True,win_size=3)
        psnr_values.append(psnr_value)
        ssim_values.append(ssim_value)
    else:
        print(f"Could not read one of the images: {img_files_gt[i]}, {img_files_render[i]}")
    # 打印当前进度
    if i%5==0 or i==min_length-1:
        print(f"Processed {i+1}/{min_length}")


# 计算平均值
avg_psnr = sum(psnr_values) / len(psnr_values)
avg_ssim = sum(ssim_values) / len(ssim_values)

print(f"Average PSNR: {avg_psnr}")
print(f"Average SSIM: {avg_ssim}")

# 输出PSNR和SSIM到文件
with open('results.txt', 'a') as f:
    f.write(f"Date: {datetime.datetime.now()}\n")
    f.write(f"GT folder: {gt_folder}\n")
    f.write(f"Render folder: {render_folder}\n")
    f.write(f"Average PSNR: {avg_psnr}\n")
    f.write(f"Average SSIM: {avg_ssim}\n")
    f.write("----------------------------------------------------------------------------------------------------------\n\n")
    

