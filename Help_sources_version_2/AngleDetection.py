# Angle detection with OpenCV

import cv2
import numpy as np

from os import listdir
from os.path import isfile, join, dirname, realpath


def draw_lines(img, lines, color=[0, 0, 255], thickness=15):
    """
    :param img: The image used as background of the lines
    :param lines: The lines to be displayed
    :param color: Line color
    :param thickness: Line thickness
    :return: nothing
    """
    if lines is None or len(lines) < 1:
        return

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def region_of_interest(img, vertices):
    """
    :param img: The image to process
    :param vertices: The vertices that describe the displayed area
    :return: The masked image
    """
    mask = np.zeros_like(img)

    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)

    return masked_image


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    :param img: The image to process
    :param rho: Rho parameter of the HoughLinesP function
    :param theta: Theta parameter of the HoughLinesP function
    :param threshold: Threshold parameter of the HoughLinesP function
    :param min_line_len: MinLineLength parameter of the HoughLinesP function
    :param max_line_gap: MaxLineGap parameter of the HoughLinesP function
    :return: Processed image
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)

    return line_img


def weighted_img(img, initial_img, alpha=0.8, beta=1.0, gamma=0.0):
    """
    :param img:The image to process
    :param initial_img: The image to process
    :param alpha:Weight alpha
    :param beta:Weight beta
    :param gamma:Weight gamma
    :return:Processed image
    """
    return cv2.addWeighted(initial_img, alpha, img, beta, gamma)


def main():
    """
    :return: Nothing
    """
    dir_path = dirname(realpath(__file__))
    path = dir_path+"\\..\\pictures"
    left_ignore_perc = 13
    right_ignore_perc = 13
    top_ignore_perc = 40
    bottom_ignore_perc = 0

    left_im = 100 / left_ignore_perc if left_ignore_perc > 0 else float("inf")
    right_im = 100 / right_ignore_perc if right_ignore_perc > 0 else float("inf")
    top_im = 100 / top_ignore_perc if top_ignore_perc > 0 else float("inf")
    bottom_im = 100 / bottom_ignore_perc if bottom_ignore_perc > 0 else float("inf")

    for f in listdir(path):
        filepath = join(path, f)

        if isfile(filepath):
            image = cv2.resize(cv2.imread(filepath), (0, 0), fx=0.5, fy=0.5)

            # ignore the unnecesarry partitions
            imshape = image.shape
            lower_left = [imshape[1] / left_im, imshape[0]-imshape[0] / bottom_im]
            lower_right = [imshape[1] - imshape[1] / right_im, imshape[0]-imshape[0] / bottom_im]
            top_left = [imshape[1] / left_im, imshape[0] / top_im]
            top_right = [imshape[1] - imshape[1] / right_im, imshape[0] / top_im]
            vertices = [np.array([lower_left, top_left, top_right, lower_right], dtype=np.int32)]
            roi_image = region_of_interest(image, vertices)

            # get a grayscale image for white recognition
            gray_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)

            # get a HSV image for yellow recognition
            hsv_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2HSV)

            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
            mask_white = cv2.inRange(gray_image, 180, 255)

            # unite the masks
            mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
            mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)

            # apply a blur, to correct image noises
            kernel_size = 27
            gauss_gray = cv2.GaussianBlur(mask_yw_image, (kernel_size, kernel_size),0)

            # detect the edges
            low_threshold = 50
            high_threshold = 150
            canny_edges = cv2.Canny(gauss_gray, low_threshold, high_threshold)

            rho = 2
            theta = np.pi / 180

            threshold = 20
            min_line_len = 30
            max_line_gap = 100

            line_image = hough_lines(canny_edges, rho, theta, threshold, min_line_len, max_line_gap)
            result = weighted_img(line_image, image)

            result = cv2.resize(result, (0, 0), fx=0.4, fy=0.4)
            mask_yw_image = cv2.resize(mask_yw_image, (0, 0), fx=0.4, fy=0.4)
            cv2.imshow('image', result)
            cv2.imshow('gray image', mask_yw_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__=="__main__":
    main()
