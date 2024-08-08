import subprocess
import argparse
import os
from pathlib import Path

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


if __name__ == '__main__':

    
    # _face_detector is used to detect faces
    cwd = os.path.abspath(os.path.dirname(__file__))
    args = parse_arguments()
    subject_name = args.subname
    testDate = args.testdate
    subDate = ''
    if args.testdate:
        subDate = args.testdate + '/'
        print(subDate)


    os.chdir(cwd)

    if "nest" in subject_name:
        subprocess.call(['python3', 'nest-video-cropping.py', subject_name, str(subDate)])
        date2 = str(subDate).replace("/", "")
        date2 = date2.replace("-", "_")

        subDir = Path('/Users/werchd01/Documents/NEST_Subjects/' + subject_name + "/" + str(subDate))
        os.chdir("/Users/werchd01/Documents/GitHub/OWLET/")
        sub_id = str(subject_name).replace("nest_", "")

        vid1 = "/Users/werchd01/Documents/NEST_Subjects/" + subject_name + "/" + str(subDate) + sub_id + "_" + date2 + ".mp4" 

        try: 
            subprocess.call(['python3', '/Users/werchd01/Documents/GitHub/OWLET/OWLET.py', "--subject_video", vid1, "--experiment_info", "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/NEST_Tasks", "--override_audio_matching"])
        except:
            print("No video")
    
    else:

        # subprocess.call(['python3', 'video-cropping.py', subject_name, str(subDate)])

        subDir = Path('/Users/werchd01/Documents/ORCA_Subjects/' + subject_name)
        os.chdir("/Users/werchd01/Documents/GitHub/OWLET/")
        sub_id = str(subject_name).replace("orca_", "")

        vid1 = "/Users/werchd01/Documents/ORCA_Subjects/" + subject_name + "/" + sub_id + "_JRAttention.mp4"
        vid2 = "/Users/werchd01/Documents/ORCA_Subjects/" + subject_name  + "/" + sub_id + "_VPC.mp4"
        vid3 = "/Users/werchd01/Documents/ORCA_Subjects/" + subject_name  + "/" + sub_id + "_ProceduralMemory.mp4"
        vid4 = "/Users/werchd01/Documents/ORCA_Subjects/" + subject_name + "/" + sub_id  + "_Cecile.mp4"
        vid5 = "/Users/werchd01/Documents/ORCA_Subjects/" + subject_name  + "/" + sub_id + "_RelationalMemory.mp4"

        try: 
            subprocess.call(['python3', '/Users/werchd01/Documents/GitHub/OWLET/OWLET.py', "--subject_video", vid1, "--experiment_info", "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/ORCA_2.0_Tasks/JRAttention", "--override_audio_matching"])
        except:
            print("No JR Attention video")
        try:
            subprocess.call(['python3', '/Users/werchd01/Documents/GitHub/OWLET/OWLET.py', "--subject_video", vid2, "--experiment_info", "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/ORCA_2.0_Tasks/VPC", "--override_audio_matching"])
        except:
            print("No VPC video")
        try:
            subprocess.call(['python3', '/Users/werchd01/Documents/GitHub/OWLET/OWLET.py', "--subject_video", vid3, "--experiment_info", "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/ORCA_2.0_Tasks/ProceduralMemory", "--override_audio_matching"])
        except:
            print("No Procedural Memory video")
        try:
            subprocess.call(['python3', '/Users/werchd01/Documents/GitHub/OWLET/OWLET.py', "--subject_video", vid4, "--experiment_info", "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/ORCA_2.0_Tasks/Cecile", "--override_audio_matching"])
        except:
            print("No Cecile video")
        try:
            subprocess.call(['python3', '/Users/werchd01/Documents/GitHub/OWLET/OWLET.py', "--subject_video", vid5, "--experiment_info", "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/ORCA_2.0_Tasks/RelationalMemory", "--override_audio_matching"])
        except:
            print("No RelationalMemory video")
