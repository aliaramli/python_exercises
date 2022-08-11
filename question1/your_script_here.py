import json
import glob
import operator
import os
import re
import fnmatch
import shutil

"""
Function to find & move files to the targeted destination
"""
def find_and_move_files(file_extension, pattern, find_path, shot_name, des_path, rename, frame_number, rename_value ):
        print ("FIND PATTERN"+ file_extension + ": " + find_path)     
        print ("DESTINATION PATH: "+ des_path)
        files = glob.glob(find_path, recursive=True )
        # checking if the directory folder 
        # exist or not.
        if not os.path.exists(des_path):
            # if directory is not present then create it.
            os.makedirs(des_path)
        # move the files to the new location
        for file in files:
            # extract frame_number from file name
            file_name = os.path.basename(file)
            if rename:
                if frame_number:
                    frame_number = re.search("(\d+)"+ file_extension +"\Z", file_name).group(1)
                    if shot_name:
                        # change the file name.
                        des_file_name = shot_name + "." +rename_value + "." + frame_number + file_extension
                elif shot_name:
                    des_file_name = shot_name + "." +rename_value + file_extension
                else:
                    des_file_name = "." +rename_value + file_extension
            else:
                des_file_name = file_name
            shutil.move(file, des_path + des_file_name)
            print("moved: " + file_name + " to: " + des_file_name)

# ENQUIRY PROJECT NAME
print('Please enter project name')
proj_name = input()
# USING JSON FILE TO DEFINE PROJECT DETAILS
try:
    f = open('proj_details.json')
    data = json.load(f)  
    proj_data = data.get(proj_name.lower());
    proj_shots = proj_data["shots"]
    paths = data["paths"]
    project_path = os.getcwd()
    
    #set path
    for path in paths:
        if path.get("client"):
            client_path = path.get("client")
        elif path.get("exr"):
            exr_path =  path.get("exr")
        elif path.get("dest_root"):
            dest_root =  path.get("dest_root")
        elif path.get("shots"):
            shots_path = path.get("shots")
        elif path.get("cc"):
            cc_path = path.get("cc")
        elif path.get("cube"):
            cube_path = path.get("cube")
        elif path.get("hdri"):
            hdri_path = path.get("hdri")
        elif path.get("video"):
            video_path = path.get("video")

    # Using linux path '[]' to handle glob case sensitive issue        
    based_pattern = "*["+proj_name.upper()+"|"+proj_name+"]*/**/"
    based_dest_path = project_path + dest_root + "PROJ_" + proj_name.upper()
    based_find_path = project_path + client_path 

    for shot_name in proj_shots:
        # Handling .exr files
        # Dest path pipeline\PROJ_ORA\shots\ban_010\plates\PlateBG\exr\
        file_extension = ".exr"
        pattern = based_pattern + "*"+ shot_name + "*/*"+ shot_name +"*"+file_extension
        find_path = based_find_path + pattern
        des_path = based_dest_path + shots_path + shot_name + exr_path        
        find_and_move_files(file_extension, pattern, find_path, shot_name, des_path, True, True, "Plate" )
#####################################################################################################
        # Handling .cc files
        # Dest path pipeline\PROJ_ORA\shots\<shot_name>\color_workflow\color_workflow\grading\grade\
        file_extension = ".cc"
        pattern = based_pattern + "*"+ shot_name +"*/sidecar/*"+ file_extension
        find_path = based_find_path + pattern
        des_path = based_dest_path + shots_path + shot_name + cc_path
        find_and_move_files(file_extension, pattern, find_path, shot_name, des_path, True, False, "MainGrade" )
###################################################################################################### 
        # HANDLING .cube FILES
        # Dest path pipeline\PROJ_ORA\shots\<shot_name>\color_workflow\color_workflow\LUTs\lut\
        file_extension  = ".cube"
        pattern = based_pattern + "*"+ shot_name +"*/sidecar/*"+ file_extension
        find_path = based_find_path + pattern
        des_path = based_dest_path + shots_path + shot_name + cube_path
        find_and_move_files(file_extension, pattern, find_path, shot_name, des_path, True, False, "MainLUT" )
###################################################################################################### 
        # HANDLING .hdri FILES
        # Dest path pipeline\PROJ_ORA\shots\<shot_name>\lighting\hdris\hdri\
        file_extension = ".hdri"
        pattern = based_pattern + "hdris/*"+ shot_name +"*"+ file_extension
        find_path = based_find_path + pattern
        des_path = based_dest_path + shots_path + shot_name + hdri_path
        find_and_move_files(file_extension, pattern, find_path, shot_name, des_path, True, False, "MainHDRI" )
###################################################################################################### 
    # HANDLING video FILES
    # Dest path pipeline\PROJ_ORA\reference
    file_extension = ".mov"
    pattern = based_pattern + "*" + file_extension
    find_path = based_find_path + pattern
    des_path = based_dest_path + video_path
    find_and_move_files(file_extension, pattern, find_path, None, des_path, False, False, "MainHDRI" )
finally:
    f.close()