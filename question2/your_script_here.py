import json

# DEFINE the window time, available machines, and simulation crucial informations. can be done in json file too.
window_time = 12
machines = [{'work_001':[], 'limit':0}, {'work_002':[], 'limit':0}, {'work_003':[], 'limit':0}]
simulations = [{"scene":"fly150.Lighting.ma", "number_of_instances":8, "number_of_frame":80, "tfi":1.5, "instance":"Pigeon"},
               {"scene":"fly160.Lighting.ma", "number_of_instances":10, "number_of_frame":60, "tfi":2, "instance":"Pigeon"}]


total_machines=len(machines)

# record the total hours assigned for each machine
total_hours = 0

# get total of all simulation hours 
for simulation in simulations:
    simulation_hours = simulation.get("number_of_instances")*simulation.get("number_of_frame")*simulation.get("tfi")/60
    print ("simulation %s total hours: %d" % (simulation.get("scene"), simulation_hours))
    total_hours = total_hours + simulation_hours
    
print ("total simulations hours %d" % total_hours)
# find the average hours for individual machine
average_hour_per_machine = total_hours/total_machines
print ("divide by %d machines %d" % (total_machines, average_hour_per_machine ))

assign_machines = {}
stop = True
# check if all simulation total hours fit the window time
if (window_time >= average_hour_per_machine):
    for simulation in simulations: ## 2 scenes
        # the specific number of instance. Eg Pigeon_001, we start with 1.
        x = 1
        # loop while we havent finish going through all available instances. Eg from Pigeon_001 - Pigeon_00X
        while x<=simulation.get("number_of_instances"):
            for machine in machines: ## 3 machines
                for key in machine: # 3 machines
                    # looping the key in machine..key (work_00x, limit). as we want the work_00x to be dynamic not static.
                    if key!= "limit":
                        # check if reach limit of average hour per machine in this case (12 hours), if yes break the loop proceed to the next available machine!
                        if machine["limit"]==average_hour_per_machine:
                            break
                        # if machine available record the schedule task
                        machine[key].append( "%s,%d,%d, %s" %(simulation.get("scene"),x, simulation.get("number_of_frame"),simulation.get("instance")))
                        x=x+1
                    else:
                        machine[key] = machine[key] + (simulation.get("number_of_frame")*simulation.get("tfi"))/60
                if x > simulation.get("number_of_instances"):
                    break

#dump the schedule task based on workstation to a json file
out_file = open("scheduled_render_task.json", "w")  
json.dump(machines, out_file, indent = 4)
print("schedule stored in scheduled_render_task.json, please run the second script which have dependency on this json file.")