import json
print("Please enter the current workstation name")
workstation = input()
# USING JSON FILE TO DEFINE PROJECT DETAILS
try:
    f = open('scheduled_render_task.json')
    datas = json.load(f)  
    for data in datas:
        for key in data:
            if key == workstation:
                for task in data[key]:
                    scene, instance_number, frame, instance = task.split(",")
                    # for simplicity since theres no division on the frame number. will use static start frame number. a more realistic way is to store the start and end frame number. 
                    start_frame = "1001"
                    end_frame = frame.rjust(3,"0").rjust(4,"1")
                    print("%s %s" % (start_frame,end_frame))
                    # Example of how to use subprocess to call run_fur_simulation.py
                    # Feel free to discard this if needed
                    import subprocess
                    fur_simulation_arguments = ['python', 'run_fur_simulation.py', '-start', start_frame, '-end', end_frame,'-instance', "%s_%s" % (instance, str(instance_number).rjust(3,"0")), '-filename', scene]
                    print(fur_simulation_arguments)
                    subprocess.call(fur_simulation_arguments)
finally:
    f.close()