import argparse
import logging
import cv2
import numpy as np
from image_stitching import ImageStitcher
from image_stitching import load_frames
from image_stitching import display

__doc__ = '''This script lets us stich images together and display or save the results'''


def parse_args():
    '''parses the command line arguments'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths',
                        type=str,
                        nargs='+',
                        help="paths to images, directories, or videos")
    parser.add_argument('--debug', action='store_true', help='enable debug logging')
    parser.add_argument('--display', action='store_true', help="display result")
    parser.add_argument('--save', action='store_true', help="save result to file")
    parser.add_argument("--save-path", default="stitched.png", type=str, help="path to save result")
    return parser.parse_args()


def estimate_blur(image):
    """
    估计图像的模糊程度，返回拉普拉斯算子的方差，方差越小越模糊
    """
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def compare_image_quality(prev_image, current_image):
    """
    比较两幅图像的质量，返回当前图像质量是否更好
    """
    prev_quality = estimate_blur(prev_image)
    current_quality = estimate_blur(current_image)
    return current_quality > prev_quality


def undistort_image(image, camera_matrix, dist_coeffs):
    """
    对图像进行去畸变处理
    """
    h, w = image.shape[:2]
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    return cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)


if __name__ == '__main__':
    args = parse_args()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)

    stitcher = ImageStitcher()
    prev_frame = None

    # 假设相机内参矩阵和畸变系数，实际应用中需要校准得到
    camera_matrix = np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.array([0.1, 0.01, 0, 0], dtype=np.float32)

    for idx, frame in enumerate(load_frames(args.paths)):
        # 去畸变处理
        frame = undistort_image(frame, camera_matrix, dist_coeffs)

        if prev_frame is not None:
            # 比较图像质量
            if not compare_image_quality(prev_frame, frame):
                logging.info(f'Skipping frame {idx} due to lower quality.')
                continue

        stitcher.add_image(frame)
        prev_frame = frame

        result = stitcher.image()

        if args.display:
            logging.info(f'displaying image {idx}')
            display('result', result)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        if args.save:
            image_name = f'result_{idx}.jpg'
            logging.info(f'saving result image on {image_name}')
            cv2.imwrite(image_name, result)

    logging.info('finished stitching images together')

    if args.save:
        logging.info(f'saving final image to {args.save_path}')
        cv2.imwrite(args.save_path, result)
        