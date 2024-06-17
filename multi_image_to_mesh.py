import numpy as np
import cv2
import open3d as o3d
from skimage.feature import ORB, match_descriptors


def extract_features(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Extract ORB features
    orb = ORB(n_keypoints=1000, fast_threshold=0.05)
    orb.detect_and_extract(gray)
    return orb.keypoints, orb.descriptors


def match_features(desc1, desc2):
    # Match descriptors between two images
    matches = match_descriptors(desc1, desc2, cross_check=True)
    return matches


def estimate_motion(kp1, kp2, matches):
    # Estimate motion between matched keypoints
    points1 = kp1[matches[:, 0]]
    points2 = kp2[matches[:, 1]]
    E, mask = cv2.findEssentialMat(points1, points2, method=cv2.RANSAC, prob=0.999, threshold=1.0)
    _, R, t, mask = cv2.recoverPose(E, points1, points2)
    return R, t


def triangulate_points(kp1, kp2, matches, R, t):
    # Triangulate points from matched keypoints
    points1 = kp1[matches[:, 0]]
    points2 = kp2[matches[:, 1]]
    proj_matrix1 = np.eye(3, 4)
    proj_matrix2 = np.hstack((R, t))
    points4D = cv2.triangulatePoints(proj_matrix1, proj_matrix2, points1.T, points2.T)
    points4D /= points4D[3]
    return points4D[:3].T


def images_to_mesh(image_paths, output_path):
    all_points = []

    for i in range(len(image_paths) - 1):
        img1 = cv2.imread(image_paths[i])
        img2 = cv2.imread(image_paths[i + 1])

        kp1, desc1 = extract_features(img1)
        kp2, desc2 = extract_features(img2)

        matches = match_features(desc1, desc2)
        R, t = estimate_motion(kp1, kp2, matches)
        points3D = triangulate_points(kp1, kp2, matches, R, t)

        all_points.append(points3D)

    all_points = np.vstack(all_points)

    # Create Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(all_points)

    # Create a mesh using Poisson reconstruction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

    # Save the mesh to an STL file
    o3d.io.write_triangle_mesh(output_path, mesh)
