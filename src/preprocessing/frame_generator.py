"""
Copyright (c) 2020 TU/e - PDEng Software Technology C2019. All rights reserved.
@Authors: Nathan Dpenha n.z.dpenha@tue.nl, Akram Shokri a.shokri@tue.nl
@Contributors: Hossein Mahdian h.mahdian@tue.nl, Samsom Beyene s.t.beyene@tue.nl
@Description:
This is a preprocessor script that is able to extract image frames from an input video.
The script is able to store the extracted image frames on disk.
The script is able to store the extracted image frames in memory (in a list).
The script is configurable to indicate the number of frames per second that must be extracted
@Last modified date: 30-11-2020
"""

import cv2
import os, sys

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
grand_parent_directory = os.path.dirname(parent_directory)
sys.path.insert(0, grand_parent_directory)
from src.preprocessing.ipreprocessing import IPreprocessing


class FrameGenerator(IPreprocessing):
    """
    This is a public class used to extract frames from videos.
    """

    __frame_per_second = None
    __CAP_PROP_FRAME_COUNT = 7

    def __init__(self, frame_per_second):
        self.__frame_per_second = frame_per_second

    def get_frames(self, video, is_rpi=False):
        """returns a list of frames from a video.
        __CAP_PROP_FRAME_COUNT constant was reassigned locally due to inaccessibility of
        several internal cv2 files from rPI.

        Args:
            video:  video object of type cv2.VideoCapture.
            is_rpi: indicates if this function is called on raspberry machine
        Returns
            list of frames based on the __frame_per_second parameter.
        """
        frames = []
        if is_rpi:
            frames, n_frame = self.__get_frames_manual(video)
        else:
            video_fps = int(video.get(self.__CAP_PROP_FRAME_COUNT))
            frame_counter = 0
            for i in range(0, video_fps):
                ret, frame = video.read()
                if frame_counter % self.__frame_per_second == 0:
                    frames.append(frame)
                frame_counter += 1
        return frames

    def get_number_of_frames(self, video, number_of_frames, is_rpi=False):
        """returns a list of frames from a video.

        Number of the returned frames will be equal to number_of_frames.
        __CAP_PROP_FRAME_COUNT constant was reassigned locally due to inaccessibility of
        several internal cv2 files from rPI.

        Args:
            video:  video object of type cv2.VideoCapture.
            number_of_frames: an integer identifying number frames to extract
            is_rpi: indicates if this function is called on raspberry machine
        Returns:
            list of frames based on the number_of_frames parameter.
        """
        if number_of_frames < 0:
            raise ValueError
        frame_array = []
        frames = []
        if is_rpi:
            frames, n_frame = self.__get_frames_manual(video)
        else:
            n_frame = int(video.get(self.__CAP_PROP_FRAME_COUNT))
        indexes = [x * n_frame / number_of_frames for x in range(number_of_frames)]

        for i in range(number_of_frames):
            if is_rpi:
                index = int(indexes[i])
                frame_array.append(frames[index])
            else:
                video.set(cv2.CAP_PROP_POS_FRAMES, indexes[i])
                ret, frame = video.read()
                frame_array.append(frame)
        return frame_array

    def __get_frames_manual(self, video):
        # initialize the total number of frames read
        total = 0
        frames = []
        # loop over the frames of the video
        while video.isOpened():
            # grab the current frame
            (grabbed, frame) = video.read()
            # check to see if we have reached the end of the
            # video
            if not grabbed:
                break
            frames.append(frame)
            # increment the total number of frames read
            total += 1
        # return the total number of frames in the video file
        return frames, total

    def save_frames(self, frame_dict, output_path, number_of_frames=None):
        """accepts a dictionary of videos with their names and
        extracts and saves frames on the disk.

        Args:
            frame_dict: A dictionary containing the names of videos and video objects of type cv2.VideoCapture.
            output_path: A path to save the generated frames for each video.
            number_of_frames: an integer identifying number frames to extract. None by default.
        """
        if output_path == '':
            project_path = os.path.abspath(os.path.join(__file__, "../../.."))
            output_path = project_path + '/prod_data/tests/test_images/generated_frames/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for filename, video in frame_dict.items():
            if number_of_frames is not None:
                frames = self.get_number_of_frames(video, number_of_frames)
            else:
                frames = self.get_frames(video)
            for i in range(0, len(frames)):
                if frames[i] is not None:
                    cv2.imwrite(output_path + "/" + filename + "-" + str(i) + ".jpg",
                                frames[i])


def main():
    fg = FrameGenerator(6)
    cap = cv2.VideoCapture("1.mp4")
    frames = fg.get_number_of_frames(cap, 10)
    print(frames.__len__())

    cap = cv2.VideoCapture("2.mp4")
    frames = fg.get_number_of_frames(cap, 10)
    print(frames.__len__())
    fg.save_frames({"video1": cap}, "./output/", 10)


if __name__ == "__main__":
    main()
