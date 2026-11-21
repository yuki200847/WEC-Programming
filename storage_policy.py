# generator $1.00/unit
# int hour, every hour ++

def battery_charging_decision_using_prediction( weather_prediction ):
    charge_decision_due_prediction = False
    if weather_prediction == "cloudy": charge_decision = True
    return charge_decision

def battery_charging_decision_using_grid( grid_price ):
    charge_decision_due_grid = False
    if
# get a number + test, if < ? , charge the battery

def battery_charging_decision_using_hours( hour_counting ):
    charge_decision_due_grid = True
    if hour_counting == 23: charge_decision_due_grid = False
    return charge_decision_due_grid
# consider night -> lower energy demand?
# bool last_hour && last_two_hour?? -> not to charge the battery

def battery_charging_decision_using_remaining( battery_remaining):
    charge_decision_due_grid = False
    if 


# fully charging ?
# idea: connect all charge_decision with and, -> all true -> charge

def charging_battery_to_a_certain_value( battery_charge_target, battery_remaining ):
    if ( battery_remaining < battery_charge_target and condition != "generator_failure" ):
        generator_use = battery_charge_target - battery_remaining
        battery_remaining = battery_charge_target

