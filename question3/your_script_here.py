import os
import glob
import itertools

def find_images():
    # define the file type extension here
    project_path = os.getcwd()
    client_path = "/images"
    based_find_path = project_path + client_path 
    based_pattern = "//*[*.exr|*.jpg]"
    find_path = based_find_path  + based_pattern
    print ("FIND PATTERN : " + find_path) 
    return [os.path.basename(x) for x in glob.glob(find_path, recursive=True )]
    
images = find_images()
print("found %d images" %len(images))

splitted_data= []

for image in images:
    splitted_data.append(image.split("."))

# Key function
#sort the splitted string data by prefix x[0]x[1], note that sometimes x[1] can also be a frame value. if x[1] is a frame value discard in lamda key, by frame number as well
# group by extension type as well theres different type with same shot name/prefix
sorted_splitted_data = sorted(splitted_data, key=lambda x: "%s%s%s%s" % (x[0],x[1] if x[1]!=x[-2] else "", x[-2], x[-1]))
key_func = lambda x: "%s%s%s" % (x[0],x[1] if x[1]!=x[-2] else "",x[-1])
for key, group in itertools.groupby(sorted_splitted_data, key_func):
    grouped = list(group)
    first_frame = grouped[0][-1]    
    last_frame = grouped[-1][-1]   
    print ("%s.%s-%s.%s" % ( "%s.%s" % (grouped[0][0],grouped[0][1]) if grouped[0][1]!=grouped[0][-2] else grouped[0][0] , grouped[0][-2],grouped[-1][-2],grouped[0][-1]))
        
        
    