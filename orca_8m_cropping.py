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


jrattn = ''
vpc = ''
srt = ''
new_tasks = ''
relmem_cecile = ''
aspectRatio = 1.77

def firebase_download(participant_ID, date):
    global fileExt, jrattn , vpc, srt, new_tasks, relmem_cecile
    

    doc_ref = db.collection("subjects").document(participant_ID)

    doc = doc_ref.get()
    bucket_name = "xxxxxxxxx.appspot.com"
    bucket = storage.bucket()
    # print(bucket)
    
    if doc.exists:
        subData = doc.to_dict()
        Path('/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' ).mkdir(parents=True, exist_ok=True)
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
                jrattn = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_JRAttention." + fileExt
                blob.download_to_filename(jrattn )
        except:
            print(participant_ID + date + '/' + "ORCA_JRAttention" + fileExt + " does not exist!")
            jrattn = ''

        try:
            source_blob_name = participant_ID + '/' +  date + "ORCA_Video2." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                vpc = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_VPC8." + fileExt
                blob.download_to_filename(vpc)
        except:
            print(participant_ID +  '/' + date +  "ORCA_VPC" + " does not exist!")
            vpc = ''

        try:
            source_blob_name = participant_ID + '/' +  date + "ORCA_Video3." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                srt = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_ProceduralMemory." + fileExt
                blob.download_to_filename(srt)
        except:
            print(participant_ID +  '/' + date +  "ORCA_ProceduralMemory" + " does not exist!")
            srt = ''

        try:
            source_blob_name = participant_ID + '/' +  date + "ORCA_Video4." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                
                new_tasks = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID +  '/8_month/'  + sub_id + "_Freeview_SocialGeo." + fileExt
                blob.download_to_filename(new_tasks)
        except:
            print(participant_ID +  '/' + date + "ORCA_Cecile" + " does not exist!")
            new_tasks = ''

        try:
            source_blob_name = participant_ID + '/' +   date + "ORCA_Video5." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                relmem_cecile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_RelationalMemory_Cecile." + fileExt
                blob.download_to_filename(relmem_cecile)
        except:
            print(source_blob_name + " does not exist!")
            relmem_cecile = ''

        try:
            source_blob_name = participant_ID + '/' +   date + "survey-data.csv"
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                surveyfile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_8m_survey_data.csv"
                blob.download_to_filename(surveyfile)
        except:
            print()

        try:
            source_blob_name = participant_ID + '/' +   date + participant_ID + "_video-times.csv"
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                surveyfile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_8m_video-times.csv"
                blob.download_to_filename(surveyfile)
            else:
                source_blob_name = participant_ID + '/' +   date  + "video-times.csv"
                blob = bucket.blob(source_blob_name)
                if blob.exists():
                    surveyfile = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_8m_video-times.csv"
                    blob.download_to_filename(surveyfile)

        except:
            print()

        try:
            source_blob_name = participant_ID + '/' +   date + "ORCA_HR_Device_On." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                hr_on = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_HR_Device_On." + fileExt
                blob.download_to_filename(hr_on)
                if fileExt == 'webm':
                    convert_to_mp4(hr_on)
                    os.remove(hr_on)
        except:
            print(source_blob_name + " does not exist!")


        try:
            source_blob_name = participant_ID + '/' +   date + "ORCA_HR_Device_Off." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                hr_off = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_HR_Device_Off." + fileExt
                blob.download_to_filename(hr_off)
                if fileExt == 'webm':
                    convert_to_mp4(hr_off)
                    os.remove(hr_off)
        except:
            print(source_blob_name + " does not exist!")
        
        try:
            source_blob_name = participant_ID + '/' +   date + "ORCA_Freeplay_NoBook." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                freeplay_nobook = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_freeplay_nobook." + fileExt
                blob.download_to_filename(freeplay_nobook)
                if fileExt == 'webm':
                    convert_to_mp4(freeplay_nobook)
                    os.remove(freeplay_nobook)
        except:
            print(source_blob_name + " does not exist!")

        try:
            source_blob_name = participant_ID + '/' +   date + "ORCA_Freeplay_book." + fileExt
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                freeplay_book = '/Users/werchd01/Documents/ORCA_Subjects/' + participant_ID + '/8_month/' + sub_id + "_freeplay_book." + fileExt
                blob.download_to_filename(freeplay_book)
                if fileExt == 'webm':
                    convert_to_mp4(freeplay_book)
                    os.remove(freeplay_book)
        except:
            print(source_blob_name + " does not exist!")


    else:
        print("No  record exists for " + participant_ID)    
        

def subName(value):
    return value
    
def date(value):
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
    
    

def crop_new_tasks(videofile, mystr):
    original_dir = Path(videofile).parent.resolve()
    filename, ext = os.path.splitext(videofile)
    if fileExt == 'webm':
        original_filename = filename + '_original.webm' 
    else:
        original_filename = filename + '_original.mp4'
    original_file = os.path.join(original_dir, original_filename)
    os.rename(videofile, original_file)
    filename = filename.replace("_Freeview_SocialGeo", "")
    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:00", "-to", "00:00:39", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_FreeviewAttn.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)   
    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:39",  "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_SocialGeo.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)  
    
def crop_relmem_cecile(videofile, mystr):
    original_dir = Path(videofile).parent.resolve()
    filename, ext = os.path.splitext(videofile)
    if fileExt == 'webm':
        original_filename = filename + '_original.webm' 
    else:
        original_filename = filename + '_original.mp4'
    original_file = os.path.join(original_dir, original_filename)
    os.rename(videofile, original_file)
    filename = filename.replace("_RelationalMemory_Cecile", "")
    subprocess.call(["ffmpeg", "-y", "-ss", "00:00:00", "-to", "00:01:40", "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_RelationalMemory.mp4"], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)   
    subprocess.call(["ffmpeg", "-y", "-ss", "00:01:40",  "-i", original_file, "-filter:v", mystr, "-r", "30", f"{filename}_Cecile.mp4"], 
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
    if jrattn != '': vid = jrattn 
    elif vpc != '': vid = vpc
    elif srt != '': vid = srt
    elif new_tasks != '': vid = new_tasks
    else: vid = relmem_cecile

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

    if jrattn != '': jrattn = convert_to_landscape(jrattn , aspectRatio)
    if vpc != '': vpc = convert_to_landscape(vpc, aspectRatio)
    if srt != '': srt = convert_to_landscape(srt, aspectRatio)
    if new_tasks != '': new_tasks = convert_to_landscape(new_tasks, aspectRatio)
    if relmem_cecile != '': relmem_cecile = convert_to_landscape(relmem_cecile, aspectRatio)
    

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
    if jrattn != '':
        subject_name = subject_name.replace("orca_", "")
        calibfilename = str(Path(jrattn ).parent.resolve()) +  '/' + subject_name
        print(calibfilename)
        cut_calibration(jrattn , calibfilename, mystr)
        crop_video(jrattn , mystr)
        
    if vpc != '': crop_video(vpc, mystr)
    if srt != '': crop_video(srt, mystr)
    if new_tasks != '': crop_new_tasks(new_tasks, mystr)
    if relmem_cecile != '': crop_relmem_cecile(relmem_cecile, mystr)
    
    
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