import cv2
import torch

from utils import get_pinhole_intrinsic_params, visualize_reprojection
from SfM import StructurefromMotion
import os
import argparse


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    return parser.parse_args()

def main():
    # set the seed to make each run deterministic
    torch.manual_seed(42)
    flags = read_args()
    dataset_name = flags.dataset

    curr_dir_path = os.getcwd()
    images_dir = os.path.join(curr_dir_path, 'dataset', dataset_name, 'rgb') 
    calibration_file_dir = os.path.join(curr_dir_path, 'dataset', dataset_name) 

    images_name = os.listdir(images_dir)

    # sort images by timestamp
    images_name = sorted(images_name, key=lambda x: float(x[:-4]))
    
    # read K from calibration file
    mtx = get_pinhole_intrinsic_params(calibration_file_dir)
    mtx = torch.tensor(mtx, requires_grad=True).detach().float()
    dist = torch.zeros(5, requires_grad=True)

    interval = 10
    img1_path = os.path.join(images_dir, images_name[0])
    img1 = cv2.imread(img1_path)
    img2_path = os.path.join(images_dir, images_name[interval])
    img2 = cv2.imread(img2_path)

    # add noise to mtx
    # Noise parameters
    # sigma = 1  # Standard deviation of the noise

    # Generate noise with the same shape as the intrinsic matrix
    # noise = torch.randn_like(mtx) * sigma

    # Add noise to the intrinsic matrix
    # mtx_noisy = mtx + noise
    # print(mtx_noisy)

    # initialize optimizer
    optimizer = torch.optim.Adam([mtx], lr=5e-3)

    num_iters = 10
    for _ in range(num_iters):

        optimizer.zero_grad()
        
        # SfM = StructurefromMotion(mtx, dist)
        SfM = StructurefromMotion(mtx, dist)

        err, R, T, point3d, src_pts, dst_pts, reproj_2d_1, reproj_2d_2 = SfM.forward(img1, img2)
        
        # print reprojection error
        print('Average reprojection error: {}'.format(err))

        # # visualize the computation graph of one pass
        # make_dot(err, params={'R': R, 'T': T, 'point3d': point3d}).render("err_torchviz", format="png")

        # visualize projection
        # visualize_reprojection(img1, img2, src_pts, dst_pts, reproj_2d_1, reproj_2d_2)

        err.backward()
        optimizer.step()

    # # create leaf nodes that require grad for R, T, point3d
    # R_opt = R.clone().detach().requires_grad_(True)
    # T_opt = T.clone().detach().requires_grad_(True)
    # point3d_opt = point3d.clone().detach().requires_grad_(True)

    # # init Trainer
    # bundle_adjuster = BundleAdjuster(R_opt, T_opt, point3d_opt, mtx, src_pts.detach(), dst_pts.detach(), optimizer='adam')

    # num_iters = 50

    # start_time = time.time()

    # for _ in range(num_iters):
    #     # train
    #     reproj_2d_1, reproj_2d_2, err = bundle_adjuster.adjust_step()

    #     # check
    #     # make_dot(err, params={'R': R_opt, 'T': T_opt, 'point3d': point3d_opt}).render("err_torchviz", format="png")

    #     # print reprojection error
    #     print('Average reprojection error: {}'.format(err))

    #     # visualize projection
    #     visualize_reprojection(img1, img2, src_pts, dst_pts, reproj_2d_1, reproj_2d_2)
    
    # end_time = time.time()
    # execution_time = end_time - start_time

    # print("Execution time: ", execution_time, " seconds")

    # point3d = point3d.detach().numpy()
    # # Visualize 3D points
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(point3d[:, 0], point3d[:, 1], point3d[:, 2], c='b', marker='o')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # plt.savefig('output/3d_points_opt.png')

    # fig2 = plt.figure()
    # new_img = draw_matches(img1, kp1[0, :, :, 2].data.cpu().numpy(), img2, kp2[0, :, :, 2].data.cpu().numpy(), matches.data.cpu().numpy(), inliers)
    # plt.imshow(new_img)
    # plt.savefig('output/matches.png')
    # plt.show()


if __name__ == '__main__':
    main()