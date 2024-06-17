import gradio as gr
import cv2
import numpy as np
import open3d as o3d
import os


def process_image(image):
    print(f"Processing image with shape: {image.shape} and dtype: {image.dtype}")

    if len(image.shape) == 2:
        # Image is grayscale
        gray_image = image
    elif len(image.shape) == 3:
        if image.shape[2] == 3:
            # Image is RGB
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif image.shape[2] == 4:
            # Image is RGBA
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        else:
            raise ValueError(f"Unexpected number of channels in input image: {image.shape[2]}")
    else:
        raise ValueError(f"Unexpected shape of input image: {image.shape}")

    # Apply edge detection
    edges = cv2.Canny(gray_image, 100, 200)
    return edges


def process_images(images):
    point_cloud = o3d.geometry.PointCloud()
    for image in images:
        edges = process_image(image)
        # Convert edges to points
        points = np.argwhere(edges > 0)
        # Add z-coordinate (depth) initialized to zero
        z = np.zeros((points.shape[0], 1))
        points = np.hstack((points, z))
        # Ensure points are of type float64
        points = points.astype(np.float64)
        print(f"Points dtype: {points.dtype}, shape: {points.shape}")  # Debug information
        point_cloud.points.extend(o3d.utility.Vector3dVector(points))
    return point_cloud


def main(images):
    if isinstance(images, list):
        # This case should handle lists of images, which shouldn't be the input here
        raise ValueError("Unexpected list of images")
    elif isinstance(images, np.ndarray):
        print(f"Received images with shape: {images.shape}, dtype: {images.dtype}")  # Debug information

        # If single image, convert to list of images
        if images.ndim == 3:
            images = [images]

        point_cloud = process_images(images)

        # Save the point cloud to a file
        o3d.io.write_point_cloud("point_cloud.ply", point_cloud)
        return "Point cloud generated and saved to 'point_cloud.ply'."
    else:
        raise ValueError("Input is not a valid image array")


iface = gr.Interface(
    fn=main,
    inputs=gr.Image(type="numpy", label="Upload Images", image_mode="RGB"),
    outputs="text",
    title="Image to Point Cloud",
    description="Upload images to generate a point cloud."
)

if __name__ == "__main__":
    iface.launch()
