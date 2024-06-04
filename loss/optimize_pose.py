
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
 @ Author     : Lichee
 @ Date       : 2024/06/03 21:17:09
 @ Description: 基于点云和视图投影的损失函数
                ● 点云数据 P，表示为一个3D点的集合。
                ● 位姿矩阵 T，表示为一个变换矩阵，用于将点云 P 从一个视图变换到另一个视图。
                我们的目标是找到一个新的位姿矩阵 T'，使得当点云 P 通过 T' 变换后投影得到的视图与实际的视图2尽可能接近。
'''

import torch
print("PyTorch version:", torch.__version__)
import torch.nn as nn
import torch.optim as optim
import numpy as np


def to_pytorch(tensor, return_type=False):
    ''' Converts input tensor to pytorch.

    Args:
        tensor (tensor): Numpy or Pytorch tensor
        return_type (bool): whether to return input type
    '''
    is_numpy = False
    if type(tensor) == np.ndarray:
        tensor = torch.from_numpy(tensor)
        is_numpy = True

    tensor = tensor.clone()
    if return_type:
        return tensor, is_numpy
    return tensor

def project_to_cam(points, camera_mat, device):
    '''
    参数：
        points: (B, N, 3)
        camera_mat: (B, 4, 4)
    '''
    # breakpoint()
    B, N, D = points.size()
    points, is_numpy = to_pytorch(points, True)
    points = points.permute(0, 2, 1)
    points = torch.cat([points, torch.ones(B, 1, N, device=device)], dim=1)

    xy_ref = camera_mat @ points

    xy_ref = xy_ref[:, :3].permute(0, 2, 1)
    xy_ref = xy_ref[..., :2] / xy_ref[..., 2:]
    
    valid_points = xy_ref.abs().max(dim=-1)[0] <= 1
    valid_mask = valid_points.unsqueeze(-1).bool()
    if is_numpy:
        xy_ref = xy_ref.numpy()
    return xy_ref, valid_mask



'''
# 假设我们有一个简单的网络来预测位姿变换
class PoseNet(nn.Module):
    def __init__(self):
        super(PoseNet, self).__init__()
        # 这里只是一个示例，实际情况下你可能需要更复杂的网络结构
        self.linear = nn.Linear(3, 3)  # 假设输入和输出位姿都是3x3矩阵平坦化后的形式

    def forward(self, x):
        # 将输入的点云坐标通过网络
        x = self.linear(x)
        return x
'''

def mse_loss(input, target):
    """
    计算均方误差损失。
    
    参数:
        input (torch.Tensor): 预测值，任意形状的张量。
        target (torch.Tensor): 真实值，与 input 形状相同的张量。
    
    返回:
        torch.Tensor: 损失值。
    """
    return nn.functional.mse_loss(input, target, reduction='mean')


def train():
    # 实例化网络、损失函数和优化器
    model = PoseNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 假设view1和view2是两个视图的点云数据
    # view1需要通过位姿变换来匹配view2
    view1 = torch.randn(1, 3, 1024)  # 示例点云数据，1个点云，每个点3个坐标，共1024个点
    view2 = torch.randn(1, 3, 1024)  # 目标点云数据

    # 训练循环
    num_epochs = 100
    for epoch in range(num_epochs):
        # 将view1的点云数据作为网络的输入
        inputs = view1.view(-1)  # 将点云平坦化为一维向量

        # 前向传播
        outputs = model(inputs).view(1, 3, 3)  # 假设输出是一个3x3的位姿矩阵

        # 将位姿矩阵应用于view1的每个点
        transformed_view1 = torch.matmul(view1, outputs.transpose(1, 2))

        # 计算损失
        loss = criterion(transformed_view1, view2)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

    # 保存模型，如果需要
    # torch.save(model.state_dict(), 'pose_net.pth')

