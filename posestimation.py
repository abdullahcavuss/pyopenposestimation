import sys
import cv2
import os
from sys import platform
import argparse
import time

# Import Openpose (Windows)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import(YOU HAVE TO CHANGE FOLDER WITH YOUR OPENPOSE PATH)
    sys.path.append('C:/Projects/openpose/build/python/openpose/Release/')
    os.environ['PATH']  = os.environ['PATH'] + ';'  + 'C:/Projects/openpose/build/x64/Release;' + 'C:/Projects/openpose/build/bin;'
    import pyopenpose as op
except ImportError as e:
    print(e)

params = dict()
params["model_folder"] = "C:/Projects/openpose/models/"

##reading keypoints
def getPoints(datum):
    getPoints.neck_x = datum.poseKeypoints[0,1,0]
    getPoints.neck_y = datum.poseKeypoints[0,1,1]
    getPoints.r_wrist_x = datum.poseKeypoints[0,4,0]
    getPoints.r_wrist_y = datum.poseKeypoints[0,4,1]
    getPoints.l_wrist_x = datum.poseKeypoints[0,7,0]
    getPoints.l_wrist_y = datum.poseKeypoints[0,7,1]
    getPoints.r_elbow_x = datum.poseKeypoints[0,3,0]
    getPoints.r_elbow_y = datum.poseKeypoints[0,3,1]
    getPoints.l_elbow_x = datum.poseKeypoints[0,6,0]
    getPoints.l_elbow_y = datum.poseKeypoints[0,6,1]
    getPoints.r_shoulder_x = datum.poseKeypoints[0,2,0]
    getPoints.r_shoulder_y = datum.poseKeypoints[0,2,1]
    getPoints.l_shoulder_x = datum.poseKeypoints[0,5,0]
    getPoints.l_shoulder_y = datum.poseKeypoints[0,5,1]
    getPoints.r_ear_x = datum.poseKeypoints[0,17,0]
    getPoints.r_ear_y = datum.poseKeypoints[0,17,1]
    getPoints.l_ear_X = datum.poseKeypoints[0,18,0]
    getPoints.l_ear_y = datum.poseKeypoints[0,18,1]

try:
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    # Read frames on webcam
    video=cv2.VideoCapture(0)
    ok, frame = video.read()
    # Process frames
    while True:
        start = time.time()
        datum = op.Datum()
        ok, frame = video.read()
        imageToProcess = frame
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])
        getPoints(datum)

        tPosition_forward= abs(getPoints.r_elbow_y - getPoints.r_shoulder_y) 
        tPosition_backward= abs(getPoints.l_elbow_y - getPoints.l_shoulder_y)
        tPosition_right = abs(getPoints.r_wrist_y - getPoints.neck_y)
        tPosition_left = abs(getPoints.l_wrist_y - getPoints.neck_y)
        tPosition_throttle = abs(getPoints.neck_x - getPoints.r_wrist_x)
        
        if (tPosition_throttle<10):
            ters = abs(getPoints.r_wrist_y - getPoints.neck_y)
            throttle = ((abs(200-ters))/10)*2 # you can mapping from here
            print(throttle)
        if(tPosition_right<20):
            print('go right')
        if(tPosition_left < 20):
            print('go left')
        if(tPosition_forward < 20):
            print('go forward')
        if(tPosition_backward < 20):
            print('go backward')
        
            
        cv2.imshow("posestimation", datum.cvOutputData)
        end = time.time()
        seconds = end - start
        fps=1/seconds
        #print(fps)
        key = cv2.waitKey(15)
        if key == 27: break
    video.release()
    cv2.destroyAllWindows()
    print("Nice dance :).")
except Exception as e:
    print(e)
    sys.exit(-1)
