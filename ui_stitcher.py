import sys
import os
import time
import subprocess
try:
	import Tkinter              # Python 2
	import ttk
except ImportError:
	import tkinter as Tkinter   # Python 3
	import tkinter.ttk as ttk
from tkFileDialog	import askopenfilenames
import fileinput



root = Tkinter.Tk()
toolbar = ttk.Frame(root)
global progress_var
progress_var = 0

def openFile():
		name=askopenfilenames()
		namelist = list(name)
		
		reference = open("ref.txt", "w")
		reference.close() #empties the ref file
		

		global outlist
		outlist = []
		for n in namelist:
			#gets just the filename, stripping away the absolute path and the extension
			outname = os.path.split(n)[1].partition('.')[0]
			#print(outname)

			#Convert video to images
			command = "ffmpeg -i " + n + " frames/"+outname+"_%05d.jpg" 
			print(command)
			subprocess.Popen(command)
			
			
			
			#Count the frames in the video, save the result to ref.txt
			#Yeah, I know, this is a bit barbaric, I should do everything in memory
			framecount = "ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1" +n+ ">> ref.txt"
			#subprocess.Popen(framecount)
			outlist.append(outname)
			
		#Export the original audio
		command = "ffmpeg -i " + namelist[0] + " ogAudio.mp3"
		subprocess.Popen(command)

		
def start():
	
	
	
	global progress_var
	progress_var = 0
	# PROJECT GENERATION
	stitch_current = "pto_gen -o prj/project.pto "
	for n in outlist:
		# add images from all cameras
		#stitch_current = stitch_current + "frames/"+n+"_"+ format(i, '05') +".jpg "
		stitch_current = stitch_current + "frames/"+n+"_00001.jpg "
	stitch_current = stitch_current + " -f 98"
	print(stitch_current)
	
	process = subprocess.Popen(stitch_current)
	process.wait()
	
	# GET CONTROL POINTS
	process = subprocess.Popen("cpfind --multirow -o prj/project.pto prj/project.pto")
	#process.wait()
	print("Here I get the control points")
	
	# Prune control points
	process = subprocess.Popen("celeste_standalone -i prj/project.pto -o prj/project.pto")
	#process.wait()
	process = subprocess.Popen("cpclean -o prj/project.pto prj/project.pto")
	#process.wait()
	process = subprocess.Popen("autooptimiser -a -l -s -o prj/project.pto prj/project.pto")
	#process.wait()
	print("Optimization done, now we stitch")
	
	# Stitch the first frame
	process = subprocess.Popen("hugin_executor --stitching --prefix=prefix prj/project.pto")
	#process.wait()
	print("Stitching done")
	
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
		
		process = subprocess.Popen("hugin_executor --stitching --prefix=" +format(i, '05')+" prj/project"+format(i, '05')+".pto")
		#process.wait()
		print("Stitching done")
	
	end()

def end():	
	reassemble = "ffmpeg -r 30 -f image2 -s 1920x1440 -i %05d.tif -i ogAudio.mp3 -shortest -vcodec libx264 -pix_fmt yuv420p -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" video_out.mp4"
	process = subprocess.Popen(reassemble)
	process.wait()
	sys.exit(1)

openButton = ttk.Button(toolbar, text="Open", command=openFile)
openButton.pack(side=Tkinter.LEFT, padx=2, pady=2)

startButton = ttk.Button(toolbar, text="Start", command=start)
startButton.pack(side=Tkinter.LEFT, padx=2, pady=2)

progressbar = ttk.Progressbar(toolbar, variable=progress_var, maximum=1000)
progressbar.pack(side=Tkinter.LEFT, padx=2, pady=2)

toolbar.pack(side=Tkinter.TOP, fill=Tkinter.X)

root.mainloop()


