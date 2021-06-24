# AI BASED VIRTUAL PAINTER

- Allows users to paint using their index finger, while in a video.

- Draw stuff.

  <img src="Utilities/Images/1.gif" style="float: left;" alt="drawing" width="400"/>

- Change colors.

  <img src="Utilities/Images/2.gif" style="float: left;" alt="drawing" width="400"/>

- Erase.

  <img src="Utilities/Images/3.gif" style="float: left;" alt="drawing" width="400"/>

- Clear the screen.

  <img src="Utilities/Images/4.gif" style="float: left;" alt="drawing" width="350"/>



## Basic Functionality (*For non-programmers*) :

- You'll enter drawing mode when only Index finger is up.

- If the middle finger is also up, you'll enter selection mode.
- Selection mode allows you to switch between colors/eraser or clear the screen.

## Brief:

This model utilizes MediaPipe's hand tracking functions to get hand landmarks(reference points) that enable the user to actually draw stuff on the screen. 

- Libraries used: OpenCV, MediaPipe, os, numpy, time
- handtrackingmodule.py is actually a class with functions like hand-landmark detector, fingers-up check and much more. We have used an instance(detector) from this class in our main program.
- Index finger tip's landmark is used to draw on the canvas.

**The steps and tacks have been explicitly mentioned in the comments of the code.**

***Dockerfile* has been provided, for Linux environment(Ubuntu)**

