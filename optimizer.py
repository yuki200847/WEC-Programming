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
last_hour=False

def reset_solar():
    '''Resets the solar energy each hour'''
    global solar_remaining
    solar_remaining=200
    return 

def charge_battery(battery_charged):
    '''adds the charged battery to the battery each hour'''
    global battery_remaining
    battery_remaining+=battery_charged
    return
      
def allocate_all_buildings(list_of_buildings, event, grid_price):
    '''use this to regroup buildings to spend all 200 units of solar energy
    list_of_buildings is a list of dictionary {"type":type, "load":demand}
    will return energy_list of dictionary {"solar":energy allocated, "battery": energy allocated, "grid": energy allocated}
     '''
    energy_list=[]
    global solar_remaining, battery_remaining
    for building in list_of_buildings:
        dem= building["load"]
        b_type= building["type"]
        batt_b4= battery_remaining
        solar_b4= solar_remaining
        if (b_type == "Lecture Hall"):
            source= battery_or_grid(dem, event, grid_price)
        else:
            source= allocate_energy(dem, event, grid_price)
        dictionary={} 
        if source==1:
            dictionary["solar"]=dem
            dictionary["grid"]=0
            dictionary["battery"]=0
        elif source==2:
            dictionary["solar"]=0
            dictionary["grid"]=dem
            dictionary["battery"]=0
        elif source==3:
            dictionary["solar"]=solar_b4
            dictionary["grid"]=dem-solar_b4
            dictionary["battery"]=0
        elif source==4:
            dictionary["solar"]=0
            dictionary["grid"]=0
            dictionary["battery"]=dem
        elif source==5:
            dictionary["solar"]=solar_b4
            dictionary["grid"]=0
            dictionary["battery"]=dem-solar_b4
        elif source==6:
            dictionary["solar"]=0
            dictionary["grid"]=dem-batt_b4
            dictionary["battery"]=batt_b4
        else:
            dictionary["solar"]=solar_b4
            dictionary["grid"]=dem- solar_b4 -batt_b4
            dictionary["battery"]=batt_b4
        energy_list.append(dictionary)
    return energy_list
            

def allocate_energy(demand, event, grid_price):
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
    if (event=="cloudy_weather") or (solar_remaining==0):
        return battery_or_grid(demand, event, grid_price)
    if (solar_remaining <= demand):
        demand-= solar_remaining
        solar_remaining=0
        return 1+ battery_or_grid(demand, event, grid_price)
    else:
        solar_remaining-=demand
        return 1
    

def battery_or_grid(demand, event, grid_price):
    '''use this if building is lecture hall 
    demand is energy demand and event is the random event
    2= grid
    4= battery
    6= battery(all_remaining)+grid'''
    global battery_remaining, last_hour
    if (event=="battery_failure"):
        return 2
    elif(event=="grid_failure"):
        battery_remaining-= demand
        return 4 
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