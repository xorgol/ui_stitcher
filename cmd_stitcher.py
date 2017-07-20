import sys
import os
import time
import subprocess

fileList = sys.argv[1:]

#Export the original audio
command = "ffmpeg -i " + fileList[0] + " ogAudio.mp3"
print(command)
command = command.split()
#proc = subprocess.check_call(command)

for n in fileList:
	#gets just the filename, stripping away the absolute path and the extension
	outname = os.path.split(n)[1].partition('.')[0]
	
	#Convert video to images
	command = "ffmpeg -i " + n + " frames/"+outname+"_%05d.jpg" 
	command = command.split()
	print(command)
	#proc = subprocess.check_call(command)
	#proc.wait()
			
print(fileList)

#proc.wait()

		

# PROJECT GENERATION
stitch_current = "pto_gen -o prj/project.pto "
for n in fileList:
	# add images from all cameras
	#stitch_current = stitch_current + "frames/"+n+"_"+ format(i, '05') +".jpg "
	#gets just the filename, stripping away the absolute path and the extension
	outname = os.path.split(n)[1].partition('.')[0]
	stitch_current = stitch_current + "frames/"+outname+"_00001.jpg "
stitch_current = stitch_current + " -f 98"
print(stitch_current)
	
#stitch_current = stitch_current.split()
#process = subprocess.check_call(stitch_current)
#process.wait()
	
# GET CONTROL POINTS
cpfind = "cpfind --multirow -o prj/project.pto prj/project.pto"
#cpfind = cpfind.split()
#process = subprocess.check_call(cpfind)
#process.wait()
print("Here I get the control points")
	
# Prune control points
celeste = "celeste_standalone -i prj/project.pto -o prj/project.pto"
#celeste = celeste.split()
#processCeleste = subprocess.check_call(celeste)
#processCeleste.wait()


cpclean = "cpclean -o prj/project.pto prj/project.pto"
#cpclean = cpclean.split()
#processClean = subprocess.check_call(cpclean)
#processClean.wait()

optimiser = "autooptimiser -a -l -s -o prj/project.pto prj/project.pto"
#optimiser = optimiser.split()
#process = subprocess.check_call(optimiser)
#process.wait()
print("Optimization done, now we stitch")
	
# Stitch the first frame
hugin = "hugin_executor --stitching --prefix=prefix prj/project.pto"
#hugin = hugin.split()
#process = subprocess.check_call(hugin)
#process.wait()
print("Stitching done")

command = stitch_current +"; " + cpfind + "; " + celeste + "; " + cpclean + "; " + optimiser + "; " + hugin
print(command)

os.system(stitch_current +"; " + cpfind + "; " + celeste + "; " + cpclean + "; " + optimiser + "; " + hugin)
	
for i in range(0, 500):
	#progress_var.set(i)
	#root.update_idletasks()
	file = open("prj/project.pto", "r")
	new_File = open("prj/project"+format(i, '05')+".pto", "w")
	data = file.read()
	newdata = data.replace("00001.jpg", ""+format(i, '05') +".jpg")
	print(newdata)
	new_File.write(newdata)

	file.close()
	new_File.close()
		
	hugin2 = "hugin_executor --stitching --prefix=" +format(i, '05')+" prj/project"+format(i, '05')+".pto"
	#hugin2 = hugin2.split()
	os.system(hugin2)
	#process.wait()
	print("Stitching done")


reassemble = "ffmpeg -r 30 -f image2 -s 1920x1440 -i %05d.tif -i ogAudio.mp3 -shortest -vcodec libx264 -pix_fmt yuv420p -vf scale=1920:-2 -strict -2 video_out.mp4"
#reassemble = reassemble.split()
print(reassemble)
os.system(reassemble)
#process.wait()
sys.exit(1)




