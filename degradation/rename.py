import os

path0 = 'F:/code1/nice-slam/Datasets/Replica/office2-lowlight/results/'
# path1 = 'F:/code/DSGN2-main/data/kitti/testing/image_3 - 副本/'

def rename(path):
    filename = os.listdir(path)
    number = 0

    for i in filename:
        new = 'depth'+"%06d.npy" % number
        number += 1
        old = i

        os.rename(path+old,path+new)


rename(path0)
# rename(path1)
