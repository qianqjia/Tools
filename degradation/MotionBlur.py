import os
import argparse
import cv2
import numpy as np
from wand.color import Color
from wand.image import Image
import random

# parse args
parser = argparse.ArgumentParser(description='Downsize images at 2x using bicubic interpolation')
parser.add_argument("-k", "--keepdims", help="keep original image dimensions in downsampled images",
                    action="store_true")
parser.add_argument('--hr_img_dir', type=str, default=r'/data/jiaqianqian/code/test/dataset',
                    help='path to high resolution image dir')
parser.add_argument('--lr_img_dir', type=str, default=r'/data/jiaqianqian/code/test/dataset',
                    help='path to desired output dir for downsampled images')
args = parser.parse_args()

hr_image_dir = args.hr_img_dir
lr_image_dir = args.lr_img_dir

print(args.hr_img_dir)

remakeType = r"/MotionBlur"

# create LR image dirs
os.makedirs(lr_image_dir + remakeType, exist_ok=True)

supported_img_formats = (".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2",
                         ".png", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tif",
                         ".tiff")

for filename in os.listdir(hr_image_dir):
    print(filename)
    if not filename.endswith(supported_img_formats):
        continue
    if "depth" in filename:
        continue

    name, ext = os.path.splitext(filename)

    with Image(filename=os.path.join(hr_image_dir, filename)) as img:
        img.motion_blur(radius=80, sigma=40, angle=random.randint(-90, 90))
        img.gaussian_blur(sigma=10)
        img.save(filename = os.path.join(lr_image_dir + remakeType, filename.split('.')[0] + ext))
