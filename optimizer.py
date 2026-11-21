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
Solar_unit= 200
battery_unit=100
grid_price=0.5
last_hour=False

def regroup_buildings(list_of_demands,event,i, last_hour=False, solar_remaining=200, battery_remaining=100):
    '''use this to regroup buildings to spend all 200 units of solar energy
    list_of_demands is a list with the demands of all buildings
    i is the index of the last lecture hall
    will return energy_list and the last 2 entries are the solar remaining and battery remaining
     '''
    energy_list=[]
    for index in range(len(list_of_demands)):
        dem= list_of_demands[index]
        if index<i:
            source= battery_or_grid(dem, event, last_hour)
        else:
            source= allocate_energy(dem, event)
        energy_list.append(source)
        if source==0:
            solar_remaining-=dem
        elif source==2:
            battery_remaining-=dem
    energy_list.append(solar_remaining)
    energy_list.append(battery_remaining)
    return energy_list
            

def allocate_energy(demand, event, last_hour=False):
    '''use this if building is not lecture hall
    demand is energy demand and event is the random event
    0 = solar
    1= grid
    2= battery'''
    if (event==cloudy_weather) or (Solar_unit<demand):
        return battery_or_grid(demand, event, last_hour)
    

def battery_or_grid(demand, event, last_hour=False):
    '''use this if building is lecture hall 
    demand is energy demand and event is the random event
    1 represents grid 
    2 represents battery'''
    if (event==battery_failure):
        return 1
    elif(event==grid_failure):
        return 2
    if (last_hour):
        if (battery_unit<demand):
            return 2
        return 1
    elif(grid_price<1):
        return 1
    return 2