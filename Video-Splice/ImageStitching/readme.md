# Image and Video Stitching

This algorithm runs through a video file, or a set of images, and stitches them together to form a single image. It can be used for scanning in large documents where the resolution from a single photo may not be sufficient. ~~``~~

## Quick Start

Run the stitching!

`python stitching.py path --display --save`

## Demonstration

[image](./examples/stitched.png)

## Modify

Consider image blurring, evaluating whether an incoming frame has a better quality than the previous one, or lens distortion.

# Note

### 1. Feature Extraction

**SIFT (Scale-Invariant Feature Transform)**

* **Principle**: The SIFT algorithm detects key points in different scale spaces and computes descriptors for these key points. These descriptors have a certain degree of invariance to image scaling, rotation, and illumination changes.

### 2. Feature Matching

* **FLANN (Fast Library for Approximate Nearest Neighbors)**
  * **Principle**: FLANN is a library for fast approximate nearest neighbor search in large datasets. In image stitching, it can quickly match feature points between two images.

**Lowe's Ratio Test**

* **Principle**: To remove incorrect matches, Lowe's ratio test compares the ratio of the distance of the nearest neighbor to the second nearest neighbor. A match is considered valid if the nearest neighbor distance is less than a threshold (e.g., 0.7) times the second nearest neighbor distance.

### 3. Compute Homography Matrix

* **RANSAC (Random Sample Consensus)**
  * **Principle**: RANSAC is an iterative algorithm used to estimate model parameters. It can robustly estimate the homography matrix even in the presence of many incorrect matches.

### 4. Image Blending

* **Perspective Transformation**
  * **Principle**: Using the computed homography matrix, perspective transformation aligns images from different viewpoints to the same coordinate system.

### 5. Image Quality Assessment

* **Laplacian Operator**
  * **Principle**: The Laplacian operator's variance is used to estimate the blurriness of an image. The smaller the variance, the blurrier the image.

### 6. Image Distortion Correction

* **Camera Intrinsic Matrix and Distortion Coefficients**
  * **Principle**: Cameras introduce distortion during image capture, which needs to be corrected using the camera's intrinsic matrix and distortion coefficients.
