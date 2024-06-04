import os
import cv2
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import torch
import numpy as np
import lpips
from torch.autograd import Variable

loss_fn_alex = lpips.LPIPS(net='alex') # best forward scores


path = './'
img_pth = './A.jpg'
gt_pth = './B.jpg'

img_rgb = cv2.imread(img_pth)
img_gt = cv2.imread(gt_pth)

if img_rgb is None:
    raise ValueError(f"Failed to load image: {img_pth}")
if img_gt is None:
    raise ValueError(f"Failed to load image: {gt_pth}")

img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
img_gt = cv2.cvtColor(img_gt, cv2.COLOR_BGR2RGB)

image_o_y = (img_rgb) / 127.5 - 1
image_gt_y = (img_gt) / 127.5 - 1

image_o_y = np.array(image_o_y)[np.newaxis, :]
image_o_y = np.transpose(image_o_y, (0, 3, 1, 2)).astype(np.float)
image_o_y = torch.tensor(image_o_y).type(torch.FloatTensor)
image_o_y = Variable(image_o_y, requires_grad=False)

image_gt_y = np.array(image_gt_y)[np.newaxis, :]
image_gt_y = np.transpose(image_gt_y, (0, 3, 1, 2)).astype(np.float)
image_gt_y = torch.tensor(image_gt_y).type(torch.FloatTensor)
image_gt_y = Variable(image_gt_y, requires_grad=False)

d3 = loss_fn_alex(image_o_y, image_gt_y).detach().numpy()
print(d3)