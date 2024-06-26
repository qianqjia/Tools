import torch
import pypose as pp
import kornia as K
from utils import compute_reprojection_error

class PixelAdjuster:

    def __init__(self, src_pts, dst_pts, K):
        """
        Constructor for BundleAdjuster class.

        Parameters:
        - R_opt: leaf node that requires grad for R
        - T_opt: leaf node that requires grad for T
        - point3d_opt: leaf node that requires grad for point3d
        - K: intrinsic matrix
        - src_pts: source points
        - dst_pts: destination points
        - optimizer: optimizer to use (adam or LBFGS)
        """

        self.src_pts = src_pts.detach().requires_grad_(True)
        self.dst_pts = dst_pts.detach().requires_grad_(True)

        self.optimizer = torch.optim.Adam([self.src_pts, self.dst_pts], lr=5e-3)
            
        self.loss = compute_reprojection_error
        self.K = K

    def adjust_step(self, pose_estimator, mode="Lie"):
        """
        Perform one adjustment step.

        """
        # Fm, _ = pose_estimator.compute_fundametal_matrix_kornia(self.src_pts, self.dst_pts)
        Fm = K.geometry.find_fundamental(self.src_pts[None, ...], self.dst_pts[None, ...])[0, ...]

        Em = K.geometry.essential_from_fundamental(Fm, self.K, self.K)
        R, T, point3d = pose_estimator.recover_pose(Em, self.src_pts, self.dst_pts, self.K)

        # LieTensor 
        P = torch.cat([R, T], dim=1)
        P_pp = pp.from_matrix(P, ltype=pp.SE3_type)
        if mode == "Lie":
            # compute reprojection error
            reproj_2d_1, reproj_2d_2, err = self.loss(point3d, self.src_pts, self.dst_pts, P=P_pp, K=self.K)
        else:
            # compute reprojection error
            reproj_2d_1, reproj_2d_2, err = self.loss(point3d, self.src_pts, self.dst_pts, P=P, K=self.K)
        
        err.backward()
        self.optimizer.step()

        return reproj_2d_1, reproj_2d_2, err, self.src_pts, self.dst_pts