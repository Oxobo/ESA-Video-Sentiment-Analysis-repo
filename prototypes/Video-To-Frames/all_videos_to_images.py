"""
Copyright (c) 2020 TU/e - PDEng Software Technology C2019. All rights reserved.
@Author: Nathan Dpenha n.z.dpenha@tue.nl
@Description: This script takes videos from one directory and extracts images and stores it in an individual directory.
@Last modified date: 05-11-2020
"""

import ffmpeg 
import os
from os import listdir
from os.path import isfile, join
from os import walk
from os import walk

input_path = './videos/' # This directory should exist with individual actor directories in it. eg ./vidoes/actor1/video.mp4
output_path = './frames/' #Path to store the frames 
videos = [] # Will contain all the list of videos to be converted.
actor_directory = [] # Will be used to keep track of which actor directroies are present in './videos' directory.
frame_per_second = 6 # set the number of frames required per second here.

print('Frames Per Second is set to: '+str(frame_per_second))
print('Images will be stored in the ' + output_path + ' directory')
print('Actors Directories Found in ' + input_path + ' are:')
for actor in os.listdir(input_path):
	if os.path.isdir(input_path+actor):
		print(actor)
		for video in os.listdir(input_path+actor):
			actor_directory.append(output_path+actor+'/'+video+'/')			
			videos.append(input_path+actor+'/'+video)
			

try: 
      
	# creating a folder named data if it does not already exist
	for dirs in actor_directory:
		if not os.path.exists(dirs):
			os.makedirs(dirs)
		if not os.path.exists(dirs):
			os.makedirs(dirs)

  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 
  

counter = -1; #used to keep track of which video is being processed.
for video in videos:
	counter = counter + 1
	print('Creating frames in --'+ actor_directory[counter])
	try:
		(No clue 
		.input(video)
		  .filter('fps', fps=frame_per_second)
		  .output(actor_directory[counter] +'/frame'+'%d.jpg', 
		          #video_bitrate='5000k',	#Uncomment based on requirement 
		          #s='64x64',				#Uncomment based on requirement 
		          #sws_flags='bilinear',	#Uncomment based on requirement 
		          start_number=0)
		  .run(capture_stdout=True, capture_stderr=True))
	except ffmpeg.Error as e:
		print('stdout:', e.stdout.decode('utf8'))
		print('stderr:', e.stderr.decode('utf8'))

