#!/usr/bin/env python3
# coding: utf-8

"""
Reference: https://github.com/YadiraF/PRNet/blob/master/utils/estimate_pose.py
"""

from math import cos, sin, atan2, asin, sqrt
import numpy as np
from .params import param_mean, param_std


def parse_pose(param):
    param = param * param_std + param_mean
    Ps = param[:12].reshape(3, -1)  # NOTE: camera matrix
    s, R, t3d = P2sRt(Ps)
    P = np.concatenate((R, t3d.reshape(3, -1)), axis=1)  # without scale；
    pose = matrix2angle(R)  # NOTE: yaw, pitch, roll
    return P, pose, s


def matrix2angle(R):
    ''' compute three Euler angles from a Rotation Matrix. Ref: http://www.gregslabaugh.net/publications/euler.pdf
    Args:
        R: (3,3). rotation matrix
    Returns:
        x: yaw
        y: pitch
        z: roll
    '''
    # assert(isRotationMatrix(R))

    if R[2, 0] != 1 or R[2, 0] != -1:
        x = asin(R[2, 0])
        y = atan2(R[2, 1] / cos(x), R[2, 2] / cos(x))
        z = atan2(R[1, 0] / cos(x), R[0, 0] / cos(x))

    else:  # Gimbal lock
        z = 0  # can be anything
        if R[2, 0] == -1:
            x = np.pi / 2
            y = z + atan2(R[0, 1], R[0, 2])
        else:
            x = -np.pi / 2
            y = -z + atan2(-R[0, 1], -R[0, 2])

    return x, y, z


def P2sRt(P): 
    #NOTE: 主点和像平面原点对应！
    ''' decompositing camera matrix P.
    Args:
        P: (3, 4). Affine Camera Matrix.
    Returns:
        s: scale factor.
        R: (3, 3). rotation matrix.
        t3d: (3,). 3d translation.
    '''
    t3d = P[:, 3]
    R1 = P[0:1, :3]
    R2 = P[1:2, :3]
    s = (np.linalg.norm(R1) + np.linalg.norm(R2)) / 2.0 # L2 norm, f=(f1+f2)/2
    r1 = R1 / np.linalg.norm(R1)
    r2 = R2 / np.linalg.norm(R2)
    r3 = np.cross(r1, r2) 
    '''
    R3 = P[2:3, :3]
    print(r3, R3/s)
    '''
    # bacause (r1 r2 r3)^T is a rotate matrix or r3 = R3/s
    # NOTE: 去掉scale很科学，scale是人脸三维到图像平面用的

    R = np.concatenate((r1, r2, r3), 0)
    return s, R, t3d


def main():
    pass


if __name__ == '__main__':
    main()
