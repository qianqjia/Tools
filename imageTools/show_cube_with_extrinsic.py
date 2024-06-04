# 使用估计得到的外参对cube进行场景重建
# 若使用自己的深度图需修改两处：line55 读取数据集路径；line68 读取数据集方式
from ntpath import join
import open3d as o3d
import numpy as np
import os
import re
import cv2

def read_array(path):
    with open(path, "rb") as fid:
        width, height, channels = np.genfromtxt(fid, delimiter="&", max_rows=1,
                                                usecols=(0, 1, 2), dtype=int)
        fid.seek(0)
        num_delimiter = 0
        byte = fid.read(1)
        while True:
            if byte == b"&":
                num_delimiter += 1
                if num_delimiter >= 3:
                    break
            byte = fid.read(1)
        array = np.fromfile(fid, np.float32)
    array = array.reshape((width, height, channels), order="F")
    return np.transpose(array, (1, 0, 2)).squeeze()

# 读取图片文件
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

# RGBD重建
def load_point_clouds(volume):
    path = "G:/Dataset/jqq/underwater/starfish/"

    depth_image_path = get_file_list(os.path.join('G:/Dataset/jqq/underwater/starfish/depth_colmap/'),
                                     extension=".bin",a='geometric')  # geometric  photometric
    depth_image_path = list(filter(lambda x: x[:-4], depth_image_path))


    # depth_image_path = get_file_list(os.path.join(path,'depth78/'),
    #                                  extension=".npy",a='r')  # geometric

    color_image_path = get_file_list(os.path.join(path, "images/"),
                                     extension=".jpg",a='frame')


    data = np.loadtxt('G:/Dataset/jqq/underwater/starfish/groundtruth.txt', delimiter=' ', dtype=np.unicode_) #groundtruth就是output_file
    pose_vecs = data[:, 1:-2].astype(np.float64)
    pose_vecs = pose_vecs[:, [4, 5, 6, 1, 2, 3, 0]]

    inv_pose = None

    for i in range(6,len(color_image_path),13):

        # depth_map = np.load(os.path.join(depth_image_path[i]))

        depth_map = read_array(depth_image_path[i])

        min_depth, max_depth = np.percentile(
            depth_map, [5, 95])
        depth_map[depth_map < min_depth] = min_depth
        depth_map[depth_map > max_depth] = max_depth

        color = cv2.imread(os.path.join(color_image_path[i]))

        color = o3d.geometry.Image(np.array(color).astype(np.uint8))
        depth = depth_map.astype(np.float32)
        depth = o3d.geometry.Image(depth)

        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
            color, depth, depth_trunc=1000.0, depth_scale=1,
            convert_rgb_to_intensity=False)  # depth_trunc:默认3.0, 大于depth_trunc的深度值被截断为0, depth_scale: 默认1000，比例深度值，深度值首先被缩放，然后被截断。
        # 深度图存储在浮点数中，以米为单位表示深度值。

        # intrinsic = o3d.camera.PinholeCameraIntrinsic(1204, 685, 1435.75, 1533.9, 602, 342.5)
        intrinsic = o3d.camera.PinholeCameraIntrinsic(3840,2160,2322.382716120409,2322.382716120409,1920,1080)

        w2c = pose_matrix_from_quaternion(pose_vecs[i])
        # c2w = np.linalg.inv(w2c)


        # if inv_pose is None:
        #     inv_pose = np.linalg.inv(c2w)  # 求逆矩阵
        #     c2w = np.eye(4)
        # else:
        #     c2w = inv_pose @ c2w
        w2c[:3, 1] *= -1
        w2c[:3, 2] *= -1

        volume.integrate(rgbd_image, intrinsic, w2c)

        # rgbd_images.append(rgbd_image)
        print(i)
        if i>50:
            break
    return volume

def pose_matrix_from_quaternion(pvec):
    """ convert 4x4 pose matrix to (t, q) """
    from scipy.spatial.transform import Rotation

    pose = np.eye(4)
    pose[:3, :3] = Rotation.from_quat(pvec[3:]).as_matrix()
    pose[:3, 3] = pvec[:3]
    return pose


from time import time

K = np.array([
    [2322.382716120409, 0.0, 1920.0],
    [0.0, 2322.382716120409, 1080.0],
    [0.0, 0.0, 1.0]
])

start_time = time()
volume = o3d.pipelines.integration.ScalableTSDFVolume(
    voxel_length=4.0 / 512.0,
    sdf_trunc=0.04,
    color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)


pcds_down = load_point_clouds(volume)

mesh = pcds_down.extract_triangle_mesh()
mesh.compute_vertex_normals()
mesh.transform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
print("花费时间：", time() - start_time)

vis = o3d.visualization.Visualizer()
coords = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.52, origin=(0,0,0))      # 显示坐标轴方向，size设定大小
vis.add_geometry(coords)
# o3d.visualization.draw_geometries([mesh,coords])
o3d.io.write_triangle_mesh("G:/Dataset/jqq/underwater/starfish/mesh/vis/1.ply", mesh)

# 显示轨迹
data = np.loadtxt('G:/Dataset/jqq/underwater/starfish/groundtruth.txt', delimiter=' ', dtype=np.unicode_)
pose_vecs = data[:, 1:-2].astype(np.float64)
pose_vecs = pose_vecs[:, [4, 5, 6, 1, 2, 3, 0]]
groundtruth_pose = data[:, 5:-2].astype(np.float64)
np.savetxt('groundtruth_pose.txt', groundtruth_pose, delimiter=' ') #相机位姿的平移部分（即相机的位置）

cam_points = []
inv_pose = None
for i in range(len(pose_vecs)):
    w2c = pose_matrix_from_quaternion(pose_vecs[i])
    c2w = np.linalg.inv(w2c)

    if inv_pose is None:
        inv_pose = np.linalg.inv(c2w)  # 求逆矩阵
        c2w = np.eye(4)
    else:
        c2w = inv_pose @ c2w
    c2w[:3, 1] *= -1
    c2w[:3, 2] *= -1

    cam_points.append(c2w[:3, 3])
    np.savetxt('cam_poses.txt', cam_points, delimiter=' ')

points = np.concatenate([cam_points], axis=0)      # cam_points是轨迹点


print(points.shape)
o3d_pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
# o3d.visualization.draw_geometries([o3d_pc])
# print(cam_points[0])

# 假设 mesh 是重建得到的网格，pose_vecs 是相机位姿
# 创建一个Visualizer对象
vis = o3d.visualization.Visualizer()
vis.create_window()

# 添加重建的网格到Visualizer对象中
vis.add_geometry(mesh)

# 设置视点参数，这里我们使用第一个相机位姿作为例子
w2c = pose_vecs[0]  # 假设 w2c 是一个4x4的位姿矩阵
intrinsic = K  # 假设 K 是之前定义的相机内参

# 创建一个PinholeCameraParameters对象
cam_params = o3d.camera.PinholeCameraParameters()
cam_params.intrinsic = o3d.camera.PinholeCameraIntrinsic(3840,2160,2322.382716120409,2322.382716120409,1920,1080)
cam_params.extrinsic = w2c

# 设置Visualizer的视点参数
vis.get_view_control().convert_from_pinhole_camera_parameters(cam_params)

# 渲染点云
vis.run()

# 捕获视窗中的截图
image = vis.capture_screen_float_buffer(do_render=True)
cv2.imwrite("captured_image.png", np.uint8(image))

# 销毁Visualizer对象
vis.destroy_window()