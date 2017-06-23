# ui_stitcher
Simple Python + Tkinter utility for stitching 360 videos using only Open Source software. Depends on FFMPEG and Hugin.
Make sure they're all in your system path. Other than that, is should work on Windows, Linux and Mac.

## Basic operation
Open your video files. They are segmented into individual frames using FFMPEG. 
Each set of frames is then passed to Hugin, which stitches them together, and generates a TIFF.
Once each frame is stitched, FFMPEG is invoked again to reassemble a video.

## Known problems
- Command line operation hasn't been implemented yet
- We just use the audio from the first video camera, we will allow **at least** to pick which one you want in the UI.
- The focal length is hardcoded to 98, which *should* be all right with GoPros and most action cameras. This should be user-settable.
- The video streams are not timelocked, so they drift in time relative to each other. You should trim your source videos to alleviate the issue, but I don't really have a fix.


# Note: I'm developing this in the open, it's not even close to functional! Check back in a couple of weeks.
