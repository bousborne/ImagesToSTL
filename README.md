# InstantMesh: Multi-Image to 3D Mesh

This project provides a tool to convert multiple images into a 3D mesh (STL file) using Python, OpenCV, Open3D, and Gradio. The tool extracts features from the images, matches them to estimate the motion, triangulates the points to generate a point cloud, and finally creates a 3D mesh.

## How It Works

### Process Overview

1. **Feature Extraction**: Uses the ORB (Oriented FAST and Rotated BRIEF) algorithm to detect and describe features in the images.
2. **Feature Matching**: Matches the features between consecutive image pairs using descriptor matching.
3. **Motion Estimation**: Estimates the relative motion (rotation and translation) between the image pairs using the Essential matrix.
4. **Triangulation**: Triangulates the matched points to create a 3D point cloud.
5. **Mesh Generation**: Uses Poisson reconstruction to create a 3D mesh from the point cloud.
6. **Export**: Exports the 3D mesh to an STL file.

## Directory Structure

InstantMesh/
│
├── requirements.txt
├── app.py
└── multi_image_to_mesh.py


## Files

- **`requirements.txt`**: Contains the dependencies required for the project.
- **`app.py`**: The main application file that sets up the Gradio interface.
- **`multi_image_to_mesh.py`**: Contains the core functions for processing images and generating the 3D mesh.

## Dependencies

The project requires the following Python packages:
- numpy
- opencv-python
- open3d
- scikit-image
- gradio

## Setup and Run Locally

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/InstantMesh.git
cd InstantMesh
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:

```
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
Install the required packages using pip:

```
pip install -r requirements.txt
```

### 4. Run the Application
Run the Gradio application locally:

```
python app.py
```

### 5. Access the Interface
Open a web browser and go to the URL provided by Gradio (usually http://localhost:7860). You will see an interface where you can upload multiple images and generate a 3D mesh (STL file).

## Gradio Interface

Gradio provides an easy-to-use interface for machine learning models. In this project, Gradio is used to create a web interface that allows users to upload multiple images and download the resulting 3D mesh.

## Gradio Interface Elements
* Inputs:
  * Image Upload: Allows multiple images to be uploaded.

* Outputs:
  * File: Provides the generated 3D mesh (STL file) for download.

## Example

Here’s an example of how the interface looks:

## Code Explanation

#### multi_image_to_mesh.py
This file contains the core functions to process images and generate a 3D mesh:

* `extract_features(image)`: Extracts ORB features from an image.

* `match_features(desc1, desc2)`: Matches descriptors between two images.

* `estimate_motion(kp1, kp2, matches)`: Estimates motion between matched keypoints.

* `triangulate_points(kp1, kp2, matches, R, t)`: Triangulates points from matched keypoints.

* `images_to_mesh(image_paths, output_path)`: Main function to process multiple images and generate a 3D mesh.

#### app.py
This file sets up the Gradio interface:

* `images_to_mesh_gradio(images)`: Handles image upload and calls the images_to_mesh function.

* `iface`: Sets up the Gradio interface with input and output specifications.
Troubleshooting

If you encounter issues running the application, ensure that all dependencies are correctly installed and that your virtual environment is activated. You can also check the console for error messages and stack traces to diagnose the problem.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Thanks to the developers of OpenCV, Open3D, and Gradio for providing the tools used in this project.

## Summary

This README file provides detailed information about how the project works, the process involved, the directory structure, setup instructions, and an explanation of the code. It also includes troubleshooting tips and acknowledgment of the tools used. You can customize and expand this README file as needed to fit your specific project and requirements.

