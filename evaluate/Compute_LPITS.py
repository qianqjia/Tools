import os
import cv2
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import torch
import numpy as np
# from skimage.measure import compare_psnr as psnr
# from skimage.measure import compare_ssim as ski_ssim
import lpips
from torch.autograd import Variable

loss_fn_alex = lpips.LPIPS(net='alex') # best forward scores


# names = ['IFCNN','DSIFT']
# filelist = os.listdir('./AGAL/')
# psnr_all = []
# ssim_all = []
# img_gt_pth = 'trainC_'
# for name in names:
#     psnr_list = []
#     ssim_list = []
#     for file in filelist:
#         img_pth='./'+name+'/'+file
#         gt_pth = './'+img_gt_pth+'/'+file
#         img_rgb = cv2.imread(img_pth)
#         img_gt = cv2.imread(gt_pth)
#
#         img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
#         img_gt = cv2.cvtColor(img_gt, cv2.COLOR_BGR2RGB)
#         image_o_y = (img_rgb) / 127.5 - 1
#         image_gt_y = (img_gt) / 127.5 - 1
#
#         image_o_y = np.array(image_o_y)[np.newaxis, :]
#         image_o_y = np.transpose(image_o_y, (0, 3, 1, 2)).astype(np.float)
#         # print(np.shape(im_input), im_input)
#         image_o_y = torch.tensor(image_o_y).type(torch.FloatTensor)
#         image_o_y = Variable(image_o_y, requires_grad=False)
#
#         image_gt_y = np.array(image_gt_y)[np.newaxis, :]
#         image_gt_y = np.transpose(image_gt_y, (0, 3, 1, 2)).astype(np.float)
#         # print(np.shape(im_input), im_input)
#         image_gt_y = torch.tensor(image_gt_y).type(torch.FloatTensor)
#         image_gt_y = Variable(image_gt_y, requires_grad=False)
#
#         d3 = loss_fn_alex(image_o_y, image_gt_y).detach().numpy()
#
#         # psnr_ = psnr(img_gt,img_rgb,data_range=255)
#         # ssim_ = ski_ssim(img_gt,img_rgb,data_range=255,multichannel=True)
#         psnr_list.append(d3)
#         # ssim_list.append(ssim_)
#     psnr_all.append(np.mean(psnr_list))
#     # ssim_all.append(np.mean(ssim_list))
#     print(name,np.mean(psnr_list))
#
# print(psnr_all,ssim_all)

path = './output/'
img_pth = '00720_0000_rgb.jpg'
gt_pth = 'frame000720.jpg'

img_rgb = cv2.imread(img_pth)
img_gt = cv2.imread(gt_pth)

img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
img_gt = cv2.cvtColor(img_gt, cv2.COLOR_BGR2RGB)
image_o_y = (img_rgb) / 127.5 - 1
image_gt_y = (img_gt) / 127.5 - 1

image_o_y = np.array(image_o_y)[np.newaxis, :]
image_o_y = np.transpose(image_o_y, (0, 3, 1, 2)).astype(np.float)
# print(np.shape(im_input), im_input)
image_o_y = torch.tensor(image_o_y).type(torch.FloatTensor)
image_o_y = Variable(image_o_y, requires_grad=False)

image_gt_y = np.array(image_gt_y)[np.newaxis, :]
image_gt_y = np.transpose(image_gt_y, (0, 3, 1, 2)).astype(np.float)
# print(np.shape(im_input), im_input)
image_gt_y = torch.tensor(image_gt_y).type(torch.FloatTensor)
image_gt_y = Variable(image_gt_y, requires_grad=False)

d3 = loss_fn_alex(image_o_y, image_gt_y).detach().numpy()
print(d3)