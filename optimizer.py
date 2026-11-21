# 7=10 buldings total:

#library:
#Lab
#Lecture Halls: Cannot be powered through Solar energy
#Student Centre
#Student Residence

#Solar generation: free 
#only 200 unit/ hour
#Battery storage: need to be recharged by backup generator
#electrical Grid : 0.5$ to 2.0$

#Backup generator:

#random events:
#cloudy_weather: Solar power cant be used
#generator_failure: Generator cannot used
#battery_failure: Battery cannot be used
#grid_failure: Grid cannot be used

#Responsibility: operates over a simulated 24-hour period, with the controller making decisions once per hour.
#At each hour, your controller will receive updated information about campus electricity demand and any unexpected operating conditions.
solar_remaining= 200
battery_remaining=100
grid_price=0.5
last_hour=False

def allocate_all_buildings(list_of_demands,event,i):
    '''use this to regroup buildings to spend all 200 units of solar energy
    list_of_demands is a list with the demands of all buildings
    i is the index of the last lecture hall
    will return energy_list and the last 2 entries are the solar remaining and battery remaining
     '''
    energy_list=[]
    global solar_remaining, battery_remaining
    for index in range(len(list_of_demands)):
        dem= list_of_demands[index]
        if index<i:
            source= battery_or_grid(dem, event)
        else:
            source= allocate_energy(dem, event)
        energy_list.append(source)
    energy_list.append(solar_remaining)
    energy_list.append(battery_remaining)
    return energy_list
            

def allocate_energy(demand, event):
    '''use this if building is not lecture hall
    demand is energy demand and event is the random event
    1 = solar
    2= grid
    3= solar(all remaining)+ grid
    4= battery
    5= solar (all remaining)+battery
    6= battery(all_remaining)+grid
    7= solar(all remaining)+battery(all remaining)+grid '''  
    global solar_remaining, battery_remaining
    if (event==cloudy_weather) or (solar_remaining==0):
        return battery_or_grid(demand, event)
    if (solar_remaining=<demand):
        demand-= solar_remaining
        solar_remaining=0
        return 1+ battery_or_grid(demand, event)
    else:
        solar_remaining-=demand
        return 1
    

def battery_or_grid(demand, event):
    '''use this if building is lecture hall 
    demand is energy demand and event is the random event
    2= grid
    4= battery
    6= battery(all_remaining)+grid'''
    global battery_remaining, last_hour, grid_price
    if (event==battery_failure):
        return 2
    elif(event==grid_failure):
        return 4 #make sure there is always enough battery for this...
    if (last_hour):
        if (battery_remaining>=demand):
            battery_remaining-=demand
            return 4
        demand-=battery_remaining
        battery_remaining=0
        return 6
    elif(grid_price<1):
        return 2
    elif (battery_remaining>=demand):
        battery_remaining-=demand
        return 4
    else:
        demand-=battery_remaining
        battery_remaining=0
        return 6