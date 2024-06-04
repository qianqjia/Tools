from PIL import Image
import os

# 打开四通道图像
image = Image.open("/data/jiaqianqian/code/test//dataset/r_20.png")

# 获取图像模式和通道数
mode = image.mode
channels = len(image.getbands())
print("图像模式:", mode)
print("通道数:", channels)

# 将图像转换为RGBA模式（如果尚未是RGBA模式）
# if image.mode != "RGBA":
#     image = image.convert("RGBA")

# 获取各个通道的图像数据
red, green, blue, alpha = image.split()

# 对各个通道进行操作
red = red.point(lambda _: 0)# 将红色通道置为全黑色
green = green.point(lambda _: 0)
blue = blue.point(lambda _: 0)

# 合并各个通道
result_image = Image.merge("RGBA", (red, green, blue, alpha))

# 保存处理后的图像
os.makedirs("/data/jiaqianqian/code/test/dataset/black", exist_ok=True)
result_image.save("/data/jiaqianqian/code/test/dataset/black/r_20.png")

print("success")