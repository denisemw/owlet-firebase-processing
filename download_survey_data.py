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

def firebase_download(participant_ID, date):
    global fileExt, jrattn , vpc, srt, new_tasks, relmem_cecile
    

    doc_ref = db.collection("subjects").document(participant_ID)

    doc = doc_ref.get()
    bucket_name = "xxxxxxxxx.appspot.com"
    bucket = storage.bucket()
    # print(bucket)
    
    if doc.exists:
       
        subData = doc.to_dict()
        
        sub_id = str(participant_ID).replace("vpc_", "")


        try:
            source_blob_name = "VPC/" + participant_ID  + '/' + date + "survey-data.csv"
            blob = bucket.blob(source_blob_name)
            if blob.exists():
                surveyfile = '/Users/werchd01/Documents/VPC_Subjects/SurveyData/' + sub_id + "_visit1_survey_data.csv"
                blob.download_to_filename(surveyfile)

        except:
            print()

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

if __name__ == '__main__':
    # _face_detector is used to detect faces
    cwd = os.path.abspath(os.path.dirname(__file__))
    convert_landscape = False
    args = parse_arguments()
    subject_name = args.subname
    subDate = args.testdate
    firebase_download(subject_name, subDate)