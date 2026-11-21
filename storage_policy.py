# generator $1.00/unit
# int hour, every hour ++

def battery_charging_decision_using_prediction( weather_prediction ):
    charge_decision_due_to_prediction = False
    if weather_prediction == "cloudy": charge_decision = True
    return charge_decision
# consider 75% accuracy

def battery_charging_decision_using_hours( hour_counting ):
    charge_decision_due_to_hours = True
    if hour_counting == 23 or hour_counting == 24: charge_decision_due_grid = False
    return charge_decision_due_to_hours
# consider night -> lower energy demand?
# bool last_hour && last_two_hour?? -> not to charge the battery

def battery_charging_decision_using_grid( grid_price ):
    charge_decision_due_to_grid = False
    if grid_price <= 2: 
        charge_decision_due_to_grid = True
        battery_charge_to_target = 100
    return charge_decision_due_to_grid

# the only function to decide charging target?
# get a number + test, if < ? , charge the battery
# 0.5 - 2
# 0.5 0.75 1 1.25 1.5 1.75 2
# predictable? logical?

def battery_charging_decision_using_remaining( battery_remaining, battery_charge_target ):
    charge_decision_due_to_remaining = False
    if battery_remaining < battery_charge_target: charge_decision_due_grid = True
    return charge_decision_due_to_remaining

# idea: connect all charge_decision with and, -> all true -> charge

def charging_battery_to_a_certain_value( battery_charge_target, battery_remaining ):
    if ( condition != "generator_failure" ):
        generator_use = battery_charge_target - battery_remaining
        battery_remaining = battery_charge_target
    return generator_use

