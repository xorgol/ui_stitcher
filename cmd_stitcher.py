import sys
import os
import time
import subprocess

fileList = sys.argv[1:]

#Export the original audio
command = "ffmpeg -i " + fileList[0] + " ogAudio.mp3"
print(command)
command = command.split()
proc = subprocess.check_call(command)

#Count the frames
command = "ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 " + sys.argv[1]
print(command)
pipe = subprocess.check_output(command.split())
returnValue = str(pipe)
frames = ""
for s in returnValue:
	if s.isdigit():
		frames = frames + s

frames = int(frames)
print(frames)

for n in fileList:
	#gets just the filename, stripping away the absolute path and the extension
	outname = os.path.split(n)[1].partition('.')[0]
	
	#Convert video to images
	command = "ffmpeg -i " + n + " frames/"+outname+"_%05d.jpg" 
	print(command)
	proc = subprocess.check_call(command.split())
			
print(fileList)

#proc.wait()

		

# PROJECT GENERATION
stitch_current = "pto_gen -o prj/project.pto "
for n in fileList:
	# add images from all cameras
	#gets just the filename, stripping away the absolute path and the extension
	outname = os.path.split(n)[1].partition('.')[0]
	stitch_current = stitch_current + "frames/"+outname+"_00001.jpg "
stitch_current = stitch_current + " -f 98"
print(stitch_current)
	

	
# GET CONTROL POINTS
cpfind = "cpfind --multirow -o prj/project.pto prj/project.pto"
print("Here I get the control points")
	
# Prune control points
celeste = "celeste_standalone -i prj/project.pto -o prj/project.pto"


cpclean = "cpclean -o prj/project.pto prj/project.pto"

optimiser = "autooptimiser -a -l -s -o prj/project.pto prj/project.pto"
print("Optimization done, now we stitch")
	
# Stitch the first frame
hugin = "hugin_executor --stitching --prefix=prefix prj/project.pto"
print("Stitching done")

command = stitch_current +"; " + cpfind + "; " + celeste + "; " + cpclean + "; " + optimiser + "; " + hugin
print(command)

subprocess.call(command.split())
	
for i in range(0, frames):
	file = open("prj/project.pto", "r")
	new_File = open("prj/project"+format(i, '05')+".pto", "w")
	data = file.read()
	newdata = data.replace("00001.jpg", ""+format(i, '05') +".jpg")
	print(newdata)
	new_File.write(newdata)

	file.close()
	new_File.close()
		
	hugin2 = "hugin_executor --stitching --prefix=" +format(i, '05')+" prj/project"+format(i, '05')+".pto"
	subprocess.call(hugin2.split())
	print("Stitching done")


reassemble = "ffmpeg -r 30 -f image2 -s 1920x1440 -i %05d.tif -i ogAudio.mp3 -shortest -vcodec libx264 -pix_fmt yuv420p -vf scale=1920:-2 -strict -2 video_out.mp4"
print(reassemble)
subprocess.call(reassemble.split())
sys.exit(1)




