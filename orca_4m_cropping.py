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
videofile2 = ''
videofile3 = ''
videofile4 = ''
videofile5 = ''
aspectRatio = 1.77

def firebase_download(participant_ID, date):
    global fileExt, videofile1, videofile2, videofile3, videofile4, videofile5
    

    doc_ref = db.collection("subjects").document(participant_ID)

    doc = doc_ref.get()
    bucket_name = "xxxxxxxxx.appspot.com"
    bucket = storage.bucket()
    # print(bucket)
    
    if doc.exists:
        subData = doc.to_dict()
        Path('/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID).mkdir(parents=True, exist_ok=True)
        sub_id = str(participant_ID).replace("orca_", "")
        
        try:
            fileExt = subData['extension']
            print(fileExt)
            print(subData['extension'])
        except:
            print("No file extension in subject record. Defaulting to webm")

        try:
            source_blob_name = participant_ID + '/' + date + "ORCA_Video1." + fileExt
            print(source_blob_name)
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                videofile1 = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_JRAttention." + fileExt
                blob.download_to_filename(videofile1)
        except:
            print(participant_ID + date + '/' + "ORCA_JRAttention" + fileExt + " does not exist!")
            videofile1 = ''

        try:
            source_blob_name = participant_ID + '/' +  date + "ORCA_Video2." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                videofile2 = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_VPC." + fileExt
                blob.download_to_filename(videofile2)
        except:
            print(participant_ID +  '/' + date +  "ORCA_VPC" + " does not exist!")
            videofile2 = ''

        try:
            source_blob_name = participant_ID + '/' +  date + "ORCA_Video3." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                videofile3 = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_ProceduralMemory." + fileExt
                blob.download_to_filename(videofile3)
        except:
            print(participant_ID +  '/' + date +  "ORCA_ProceduralMemory" + " does not exist!")
            videofile3 = ''

        try:
            source_blob_name = participant_ID + '/' +  date + "ORCA_Video4." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                
                videofile4 = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_Cecile." + fileExt
                blob.download_to_filename(videofile4)
        except:
            print(participant_ID +  '/' + date + "ORCA_Cecile" + " does not exist!")
            videofile4 = ''

        try:
            source_blob_name = participant_ID + '/' +   date + "ORCA_Video5." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                videofile5 = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_RelationalMemory." + fileExt
                blob.download_to_filename(videofile5)
        except:
            print(participant_ID +   '/' + date +  "ORCA_RelationalMemory" + " does not exist!")
            videofile5 = ''
        try:
            source_blob_name = participant_ID + '/' +   date + "survey-data.csv"
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                surveyfile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_4m_survey_data.csv"
                blob.download_to_filename(surveyfile)
        except:
            print()
        try:
            source_blob_name = participant_ID + '/' +   date + participant_ID + "_video-times.csv"
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                surveyfile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_4m_video-times.csv"
                blob.download_to_filename(surveyfile)
            else:
                source_blob_name = participant_ID + '/' +   date  + "video-times.csv"
                blob = bucket.blob(source_blob_name)
                if blob.exists():
                    surveyfile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/' + sub_id + "_4m_video-times.csv"
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
        print("calibration", videofile)
        subprocess.call(["ffmpeg", "-y", "-ss", "00:00:02", "-to", "00:00:17", "-i", videofile, "-filter:v", mystr, "-r", "30", f"{filename}_calibration.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        
def convert_to_mp4(videofile):
    filename, ext = os.path.splitext(videofile)
    subprocess.call(["ffmpeg", "-y", "-i", videofile,  "-r", "30", f"{filename}.mp4"], 
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

    if fileExt == 'webm':
        convert_to_mp4(original_file)
        os.remove(original_file)
        
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
    elif videofile2 != '': vid = videofile2
    elif videofile3 != '': vid = videofile3
    elif videofile4 != '': vid = videofile4
    else: vid = videofile5

    filename, ext = os.path.splitext(vid)
    if fileExt == "webm": convert_to_mp4(vid)

    vid = filename + ".mp4"
    print("VIDEO NAME IS ", vid)

    cap = cv2.VideoCapture(vid) 

    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = frame.shape        
    aspectRatio = width/height
    print("aspect ratio: ", aspectRatio)
    cap.release()

    if videofile1 != '': videofile1 = convert_to_landscape(videofile1, aspectRatio)
    if videofile2 != '': videofile2 = convert_to_landscape(videofile2, aspectRatio)
    if videofile3 != '': videofile3 = convert_to_landscape(videofile3, aspectRatio)
    if videofile4 != '': videofile4 = convert_to_landscape(videofile4, aspectRatio)
    if videofile5 != '': videofile5 = convert_to_landscape(videofile5, aspectRatio)
    

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
            adult_index = 0
        else:
            face_index = 0
            adult_index = 1
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


                #### alter if an adult's face is detected
                if len(faces) > 1:
                    startY_adult = faces[adult_index].top()
                    endY_adult = faces[adult_index].bottom()
                    face_h_adult = endY_adult - startY_adult
                    center_y_adult = startY_adult + (face_h_adult / 2)
                    if h > center_y_adult:
                        max_h = center_y_adult
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
    if videofile1 != '':
        subject_name = subject_name.replace("orca_", "")
        calibfilename = str(Path(videofile1).parent.resolve()) +  '/' + subject_name
        print(calibfilename)
        cut_calibration(videofile1, calibfilename, mystr)
        crop_video(videofile1, mystr)
        
    if videofile2 != '': crop_video(videofile2, mystr)
    if videofile3 != '': crop_video(videofile3, mystr)
    if videofile4 != '': crop_video(videofile4, mystr)
    if videofile5 != '': crop_video(videofile5, mystr)
    
    
#     filename, ext = os.path.splitext(videofile)


    
    
#     # print(ff_start, ff_end, mystr, videofile, filename)
    
#     subprocess.call(["ffmpeg", "-ss", "00:00:02", "-to", "00:00:15", "-i", videofile, "-filter:v", mystr, f"{filename}_calibration.mp4"], 
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.STDOUT)


        
    # subprocess.call(["ffmpeg", "-ss", ff_end, "-i", videofile, "-filter:v", mystr, f"{filename}_tasks.mp4"], 
    #             stdout=subprocess.DEVNULL,
    #             stderr=subprocess.STDOUT)
    
#     subprocess.call(["ffmpeg", "-i", videofile, "-filter:v", mystr, f"{filename}_cropped.mp4"], 
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.STDOUT)