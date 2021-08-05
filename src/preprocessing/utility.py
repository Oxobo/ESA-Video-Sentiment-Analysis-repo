"""
Copyright (c) 2020 TU/e - PDEng Software Technology C2019. All rights reserved.
@ Authors: Yusril Maulidan Raji y.m.raji@tue.nl
Last modified date: 01-12-2020
"""

import cv2


class Utility:
    """
    This is a stateless utility class that contain common operations for preprocessing module.
    """
    @staticmethod
    def resize_image(image, percent):
        """resizes an image based on the passed percent parameter

        Args:
            image: image that will be resized
            percent: the end size of the resized image based on percentage

        Returns:
            the resized image
        """
        # calculate the new size
        width = int(image.shape[1] * percent)
        height = int(image.shape[0] * percent)
        new_size = (width, height)
        # resize image
        image = cv2.resize(image, new_size)
        return image

    @staticmethod
    def calculate_resize_percent(img_height, img_height_threshold=216):
        """calculates the resize percentage of an image based on the image height threshold
        Args:
            img_height: image's height that will be resized
            img_height_threshold: optional. The default value is 216

        Returns:
            the resize percent in decimal format
        """
        return img_height_threshold / img_height if img_height > img_height_threshold else 1.
