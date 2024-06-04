import os
from moviepy.editor import VideoFileClip

def convert_mp4_to_gif(mp4_path, gif_path, fps=15):
    clip = VideoFileClip(mp4_path)
    subclip = clip.subclip(0, clip.duration)  # 截取整个视频
    subclip.write_gif(gif_path)
    subclip.close()

# 获取视频文件所在的文件夹
folder_path = 'D:/Code/ZoomLab_NeRF'

# 遍历文件夹下的所有视频文件
for filename in os.listdir(folder_path):
    if filename.endswith('.mp4'):
        # 构造视频文件的路径
        mp4_path = os.path.join(folder_path, filename)
        # 构造gif文件的路径
        gif_path = os.path.splitext(mp4_path)[0] + '.gif'
        # 调用函数进行转换
        convert_mp4_to_gif(mp4_path, gif_path)

