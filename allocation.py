# 7-10 buildings total

# Solar generation: free, maximum 200 units/hour
# Battery storage: recharged by backup generator
# Electrical grid: $0.50 to $2.00 per unit

solar_remaining = 200
battery_remaining = 100
last_hour = False


def reset_solar():
    '''Resets the solar energy each hour'''
    global solar_remaining
    solar_remaining = 200
    return


def charge_battery(battery_charged):
    '''Adds the charged battery to the battery each hour'''
    global battery_remaining
    battery_remaining += battery_charged
    return


def allocate_all_buildings(list_of_buildings, event, grid_price):
    '''Allocate energy to all buildings.

    list_of_buildings is a list of dictionaries:
    {"type": type, "load": demand}

    Returns a list of dictionaries:
    {"solar": ..., "battery": ..., "grid": ...}
    '''
    energy_list = []
    global solar_remaining, battery_remaining

    for building in list_of_buildings:
        dem = building["load"]
        b_type = building["type"]
        batt_b4 = battery_remaining
        solar_b4 = solar_remaining

        if b_type == "lecture_hall":
            source = battery_or_grid(dem, event, grid_price)
        else:
            source = allocate_energy(dem, event, grid_price)

        dictionary = {}

        if source == 1:
            dictionary["solar"] = dem
            dictionary["grid"] = 0
            dictionary["battery"] = 0

        elif source == 2:
            dictionary["solar"] = 0
            dictionary["grid"] = dem
            dictionary["battery"] = 0

        elif source == 3:
            dictionary["solar"] = solar_b4
            dictionary["grid"] = dem - solar_b4
            dictionary["battery"] = 0

        elif source == 4:
            dictionary["solar"] = 0
            dictionary["grid"] = 0

            # FIX: Only report battery energy actually used
            dictionary["battery"] = batt_b4 - battery_remaining

        elif source == 5:
            dictionary["solar"] = solar_b4
            dictionary["grid"] = 0

            # FIX: Only report battery energy actually used
            dictionary["battery"] = batt_b4 - battery_remaining

        elif source == 6:
            dictionary["solar"] = 0
            dictionary["grid"] = dem - batt_b4
            dictionary["battery"] = batt_b4

        else:
            dictionary["solar"] = solar_b4
            dictionary["grid"] = dem - solar_b4 - batt_b4
            dictionary["battery"] = batt_b4

        energy_list.append(dictionary)

    return energy_list


def allocate_energy(demand, event, grid_price):
    '''Allocate energy if the building is not a lecture hall.

    1 = solar
    2 = grid
    3 = solar + grid
    4 = battery
    5 = solar + battery
    6 = battery + grid
    7 = solar + battery + grid
    '''
    global solar_remaining, battery_remaining

    if (event == "cloudy_weather") or (solar_remaining == 0):
        return battery_or_grid(demand, event, grid_price)

    if solar_remaining <= demand:
        demand -= solar_remaining
        solar_remaining = 0
        return 1 + battery_or_grid(demand, event, grid_price)

    else:
        solar_remaining -= demand
        return 1


def battery_or_grid(demand, event, grid_price):
    '''Allocate energy from battery or grid.

    2 = grid
    4 = battery
    6 = battery + grid
    '''
    global battery_remaining

    if event == "battery_failure":
        return 2

    elif event == "grid_failure":
        # FIX: Never use more battery than is available
        battery_used = min(demand, max(0, battery_remaining))
        battery_remaining -= battery_used
        return 4

    if last_hour:
        if battery_remaining >= demand:
            battery_remaining -= demand
            return 4

        demand -= battery_remaining
        battery_remaining = 0
        return 6

    elif grid_price < 1:
        return 2

    elif battery_remaining >= demand:
        battery_remaining -= demand
        return 4

    else:
        demand -= battery_remaining
        battery_remaining = 0
        return 6