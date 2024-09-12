#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 16:10:21 2023

@author: werchd01
"""

import cv2
import dlib
import os
import numpy as np
import subprocess
import argparse
# import librosa
# from scipy import signal
from pathlib import Path
import sys

import firebase_admin
from firebase_admin import credentials, storage, firestore

cred = credentials.Certificate("/Users/werchd01/owlet-app-firebase-adminsdk-lmpui-faf5ca67c2.json")
app = firebase_admin.initialize_app(cred, {'storageBucket': 'owlet-app.appspot.com'})
db = firestore.client()
fileExt = 'webm'


videofile1 = ''

aspectRatio = 1.77

def firebase_download(participant_ID, date):
    global fileExt, videofile1
    

    doc_ref = db.collection("subjects").document(participant_ID)

    doc = doc_ref.get()
    bucket = storage.bucket()
    # print(bucket)
    
    if doc.exists:
        subData = doc.to_dict()
        Path('/Users/werchd01/Documents/VPC_Subjects/' + participant_ID + "/" + date).mkdir(parents=True, exist_ok=True)
        sub_id = str(participant_ID).replace("vpc_", "")
        date2 = str(date).replace("/", "")
        date2 = date2.replace('-', "_")
        try:
            fileExt = subData['extension']

        except:
            print("No file extension in subject record. Defaulting to webm")

        try:
            bucketname = "VPC/" + participant_ID 
            source_blobs = bucket.list_blobs(prefix=bucketname)
            source_blob_name1 = source_blobs[0]
            blob = bucket.blob(source_blob_name1)
            if blob.exists():
                if "baseline" in subject_name:
                    videofile1 = '/Users/werchd01/Documents/VPC_Subjects/' + participant_ID + '/' + "baseline/" + sub_id + "_baseline." + fileExt
                else:
                    videofile1 = '/Users/werchd01/Documents/VPC_Subjects/' + participant_ID + '/' + "test/" + sub_id + "_test." + fileExt
                blob.download_to_filename(videofile1)
        except:
            # try:
            #     fileExt = "mp4"
            #     source_blob_name = "NestStudy/" + participant_ID + '/' + date + "NestStudy_Video1.mp4"
            #     print(source_blob_name)
            #     blob = bucket.blob(source_blob_name)
            #     if blob.exists():
            #         videofile1 = '/Users/werchd01/Documents/NEST_Subjects/' + participant_ID + '/' + date + sub_id + "_Video1_" + date2 + ".mp4" 
            #         blob.download_to_filename(videofile1)
            # except:

            print(participant_ID + date + '/' + "Nest Video1" + fileExt + " does not exist!")
            videofile1 = ''

      
        try:
            
            source_blob_name = "VPC/" +  participant_ID + '/' +   date + "survey-data.csv"
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                surveyfile = '/Users/werchd01/Documents/VPC_Subjects/' + participant_ID + '/' + sub_id + "_survey_data.csv"
                blob.download_to_filename(surveyfile)
        except:
            print()

    else:
        print("No  record exists for " + participant_ID)    
        

def subName(value):
    # if not (value.endswith('.mp4') or value.endswith('.mov') or value.endswith('.m4v')):
    #     raise argparse.ArgumentTypeError(
    #         'video file must be of type *.mp4, *.mov, or *.m4v')
    return value
def date(value):
    # if not (value.endswith('.mp4') or value.endswith('.mov') or value.endswith('.m4v')):
    #     raise argparse.ArgumentTypeError(
    #         'video file must be of type *.mp4, *.mov, or *.m4v')
    return value

def parse_arguments():
    parser = argparse.ArgumentParser(description='OWLET - Online Webcam Linked Eye Tracker')
    
    parser.add_argument('subname', type=subName, help='the subject to process')
    parser.add_argument('testdate', type=date, help='the subject to process')

    args = parser.parse_args()
    
    return args


    
def cut_calibration(videofile, filename, mystr):
        # mystr = "fps=30"
    filename = filename.replace("_baseline", "")
    filename = filename.replace("_test", "")

    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:02", "-to", "00:00:10", "-i", videofile, "-filter:v", mystr, "-r", "30", f"{filename}_calibration.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        
def convert_to_mp4(videofile):
    filename, ext = os.path.splitext(videofile)
    subprocess.call(["ffmpeg", "-y", "-i", videofile,  "-r", "30", f"{filename}.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
    
def crop_familiarization(videofile, mystr):
    original_dir = Path(videofile).parent.resolve()
    filename, ext = os.path.splitext(videofile)
    if fileExt == 'webm':
        original_filename = filename + '_original.webm' 
    else:
        original_filename = filename + '_original.mp4'
    original_file = os.path.join(original_dir, original_filename)
    os.rename(videofile, original_file)
    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:10", "-to", "00:01:28", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_cecile1.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)   
    subprocess.call(["ffmpeg", "-y", "-ss", "00:01:28", "-to", "00:01:58", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_vpc_baseline.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)  
    
def crop_test(videofile, mystr):
    original_dir = Path(videofile).parent.resolve()
    filename, ext = os.path.splitext(videofile)
    if fileExt == 'webm':
        original_filename = filename + '_original.webm' 
    else:
        original_filename = filename + '_original.mp4'
    original_file = os.path.join(original_dir, original_filename)
    filename = filename.replace("_test", "")
    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:40", "-to", "00:01:28", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_cecile2.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)   
    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:10", "-to", "00:00:40", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_vpc_test.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)  


    
def crop_video(videofile, mystr):
    original_dir = Path(videofile).parent.resolve()
    filename, ext = os.path.splitext(videofile)
    if fileExt == 'webm':
        original_filename = filename + '_original.webm' 
    else:
        original_filename = filename + '_original.mp4'
    original_file = os.path.join(original_dir, original_filename)
    os.rename(videofile, original_file)
    subprocess.call(["ffmpeg", "-y", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        
def convert_to_landscape(videofile, vidAspectRatio):

    original_file = videofile
    print(vidAspectRatio, " video aspect")
  
    if vidAspectRatio < 1.75:
        original_dir = Path(videofile).parent.resolve()
        filename, ext = os.path.splitext(videofile)
        original_filename = filename + '_original_portrait.mp4'
        original_file = os.path.join(original_dir, original_filename)
        os.rename(videofile, original_file)
        newfilename = filename + '.mp4'
        ideal_width = int(height / .5625)
        dif_width = ideal_width - width
        padding = int(dif_width/2)
        ffmpeg_str = "[0]pad=w=%s:h=%s:x=%s:y=%s:color=black"  % (ideal_width, height, padding, 0)
        ff_path = "ffmpeg/ffmpeg"
        cwd = os.path.abspath(os.path.dirname(__file__))
        if hasattr(sys, '_MEIPASS'):
            ffmpeg_path = os.path.join(sys._MEIPASS, ff_path)
        else:
            ffmpeg_path = os.path.join(cwd, ff_path)

                
        subprocess.call([ffmpeg_path, "-y", "-i", original_file, "-filter_complex", ffmpeg_str, "-r", "30", f"{newfilename}"], 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        original_file = os.path.abspath(newfilename)
        print("original_file", original_file)
    return original_file

    
if __name__ == '__main__':
    # _face_detector is used to detect faces
    cwd = os.path.abspath(os.path.dirname(__file__))
    convert_landscape = False
    args = parse_arguments()
    subject_name = args.subname
    subDate = args.testdate
    firebase_download(subject_name, subDate)

    face_detector = dlib.get_frontal_face_detector()
    if videofile1 != '': vid = videofile1


    filename, ext = os.path.splitext(videofile1)
    if fileExt == "webm": convert_to_mp4(videofile1)

    vid = filename + ".mp4"
    print("VIDEO NAME IS ", videofile1)

    cap = cv2.VideoCapture(videofile1) 

    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = frame.shape        
    aspectRatio = width/height
    print("aspect ratio: ", aspectRatio)
    cap.release()

    if videofile1 != '': videofile1 = convert_to_landscape(videofile1, aspectRatio)

    

    found_face = 0
    xList = []
    wList = []
    yList = []
    hList = []
    cap = cv2.VideoCapture(vid) 

    # calibfilename = str(os.path.abspath(videofile1)) + subject_name
    
    while (cap.isOpened() and found_face < 100):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
    
        if (ret == False):
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape
        faces = face_detector(frame)
                
        ## if there are two faces detected, take the lower face
        if len(faces) > 1 and (faces[1].bottom() > faces[0].bottom()):
            face_index = 1
        else:
            face_index = 0
        if len(faces) > 0:
            startY = faces[face_index].top()
            endY = faces[face_index].bottom()
            startX = faces[face_index].left()
            endX = faces[face_index].right()
            face_h = endY - startY
            center_y = startY + (face_h / 2)
            center_x = startX + ((endX - startX) / 2)
            max_w = width
            max_h = height
    
            # verify that the face isn't a stimulus (by checking if the found face is super small)
            if face_h / height > .1:
                found_face += 1  
    
                # changing aspect ratio to 16x9     
                if max_w/max_h > 1.8:
                    max_w = int(max_h / .5625)
                elif max_w/max_h < 1.75:
                    max_h = int(max_w * .5625)
                    
                # zooms in on face if face is too far
                if face_h / max_h < .4:
                    max_h = int(face_h / .4)
                    max_w = int(1.7777*max_h)
                y = int(center_y - int(max_h/2))
                h = int(center_y + int(max_h/2))
                x = center_x - int(max_w/2)
                w = center_x + int(max_w/2)
                
                # make sure new coords aren't out of bounds
                if y < 0: 
                    diffY = abs(y)
                    y = 0
                    h = h + diffY
                if h > height:
                    diffH = h - height
                    h = height
                    y = y - diffH
                if x < 0: 
                    diffX = abs(x)
                    x = 0
                    w = w + diffX
                if w > width:
                    diffW = w - width
                    w = width
                    x = x - diffW
                xList.append(x)
                yList.append(y)
                wList.append(w)
                hList.append(h)
        
    cap.release()
    cv2.destroyAllWindows()
    print("yup")
    
    if len(xList) < 50:
        if width/height > 1.8:
            width = int(height / .5625)
        elif width/height < 1.75:
            height = int(width * .5625)
        w, h, x, y = width, height, 0, 0
    
    else:    
        xList2=np.array(xList)
        x = int(sum(xList2)/len(xList2))
        
        xList2=np.array(yList)
        y = int(sum(xList2)/len(xList2))
        
        xList2=np.array(wList)
        w = int(sum(xList2)/len(xList2)) - x
        
        xList2=np.array(hList)
        h = int(sum(xList2)/len(xList2)) - y

    mystr = "crop=%s:%s:%s:%s" % (w, h, x, y)
    myDate = str(subDate)
    myDate = myDate.replace("/", "")
    myDate = myDate.replace('-', "_")
    
    if videofile1 != '':
        subject_name = subject_name.replace("vpc_", "")
        calibfilename = str(Path(videofile1).parent.resolve()) +  '/' + subject_name
        print(calibfilename, myDate)
        cut_calibration(videofile1, calibfilename, mystr)
    
        if 'baseline' in videofile1:
            crop_familiarization(videofile1, mystr)
            # do something
        else:
            crop_test(videofile1, mystr)
            #do something
      
