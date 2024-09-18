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

    subprocess.call(['python3', 'mice_baseline_cropping.py', subject_name, str(subDate)])
    PATH_TO_DATA = '/Users/werchd01/Documents/VPC_Subjects/'
    PATH_TO_OWLET = "/Users/werchd01/Documents/GitHub/OWLET/"
    PATH_TO_TASKS = "/Users/werchd01/Documents/GitHub/OWLET-preprocessing/MICE_baseline_tasks/"

    subDir = Path(PATH_TO_DATA + subject_name)
    os.chdir(PATH_TO_OWLET)
    sub_id = str(subject_name).replace("vpc_", "")

    vid1 = PATH_TO_DATA + subject_name + "/" + "baseline" + "/" + sub_id + "_cecile.mp4"
    vid2 = PATH_TO_DATA + subject_name + "/" + "baseline" + "/" + sub_id + "_vpc_baseline.mp4"
   

    owlet_command = PATH_TO_OWLET + 'OWLET.py'
    vpc_baseline_path =  PATH_TO_TASKS + 'vpc_baseline'
    cecile_path = PATH_TO_TASKS + 'Cecile'


    try: 
        subprocess.call(['python3', owlet_command, "--subject_video", vid1, "--experiment_info", cecile_path, "--override_audio_matching"])
        
        subprocess.call(['python3', owlet_command, "--subject_video", vid2, "--experiment_info", vpc_baseline_path, "--override_audio_matching"])

    except:
        print("No video")
    

