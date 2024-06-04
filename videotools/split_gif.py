from PIL import Image

def split_gif(filename, output_left, output_right):
    # 打开GIF文件
    gif = Image.open(filename)

    # 获取GIF的帧数
    num_frames = gif.n_frames

    # 获取GIF的延迟时间（以毫秒为单位）
    durations = []
    for i in range(num_frames):
        gif.seek(i)
        durations.append(gif.info.get('duration', 100))

    # 创建一个新的GIF文件对象，用于保存左边的帧
    gif_left = Image.new('RGBA', (gif.width // 2, gif.height))

    # 创建一个新的GIF文件对象，用于保存右边的帧
    gif_right = Image.new('RGBA', (gif.width // 2, gif.height))

    # 逐帧处理GIF文件
    for i in range(num_frames):
        gif.seek(i)

        # 将当前帧裁剪成左右两部分
        frame_left = gif.crop((0, 0, gif.width // 2, gif.height))
        frame_right = gif.crop((gif.width // 2, 0, gif.width, gif.height))

        # 将左半部分的帧添加到左边的GIF文件对象中
        gif_left.paste(frame_left, (0, 0))

        # 将右半部分的帧添加到右边的GIF文件对象中
        gif_right.paste(frame_right, (0, 0))

        # 设置左右两个GIF文件的延迟时间
        gif_left.info['duration'] = durations[i]
        gif_right.info['duration'] = durations[i]

        # 设置左右两个GIF文件的帧编号
        gif_left.info['loop'] = 0 if i == num_frames - 1 else -1
        gif_right.info['loop'] = 0 if i == num_frames - 1 else -1

        # 保存左边的GIF文件
        gif_left.save(output_left, save_all=True, append_images=[gif_left], loop=0)

        # 保存右边的GIF文件
        gif_right.save(output_right, save_all=True, append_images=[gif_right], loop=0)

    print("GIF文件已成功裁剪并保存为左右两个文件。")

# 输入原始GIF文件路径和拆分后的左侧、右侧GIF文件路径
gif_path = './1/outputSidebySideIUI3.gif'
left_gif_path = './1/outputSidebySideIUI3_left.gif'
right_gif_path = './1/outputSidebySideIUI3_right.gif'

# 执行拆分操作
split_gif(gif_path, left_gif_path, right_gif_path)