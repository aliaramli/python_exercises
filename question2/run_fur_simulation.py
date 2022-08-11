# Mock script to simulate fur simulation script
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-start", type=int, required=True, help="Start frame for simulation")
parser.add_argument("-end", type=int, required=True, help="Start frame for simulation")
parser.add_argument("-instance", type=str, required=True, help="Instance in scene file to simulate")
parser.add_argument("-filename", type=str, required=True, help="Filename")
args = parser.parse_args()

start_frame = args.start
end_frame = args.end
instance_name = args.instance
file_name = args.filename

for f in xrange(start_frame, end_frame+1):
    print("Simulating instance={instance} of {file} Frame:{frame}".format(
                                                                   instance=instance_name,
                                                                   file=file_name,
                                                                   frame=f
                                                                    ))

