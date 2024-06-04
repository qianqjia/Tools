import shutil
import os
import re
from ntpath import join


def sorted_alphanum(file_list_ordered):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(file_list_ordered, key=alphanum_key)

def get_file_list(path, extension=None,a=None):
    if extension is None:
        file_list = [path + f for f in os.listdir(path) if os.path.isfile(join(path, f))]
    else:
        file_list = [
            path + f
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] == extension and a in os.path.splitext(f)[0]
        ]

    file_list = sorted_alphanum(file_list)
    return file_list


depth_image_path = get_file_list(os.path.join('G:/Dataset/jqq/underwater/starfish/images/stereo/depth_maps/'),
                                     extension=".bin",a='geometric')  # geometric  photometric

print(depth_image_path)

for i in range(len(depth_image_path)):
    c = '%s'%(depth_image_path[i][60:])

    shutil.copyfile(depth_image_path[i],
                    'G:/Dataset/jqq/underwater/starfish/depth_colmap/%s'%c)
