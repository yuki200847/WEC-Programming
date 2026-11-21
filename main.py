import json
import socket

import storage_policy
import optimizer



HOST = "localhost"
PORT = 8800


def decide(data, state):
    loads = data["loads"]
    event = data["random_event"]
    forecast = data["forecast"]
    grid_price = data["grid_price"]
    hour = state["hour"]
    battery_remaining = state["battery"]

    # Call functions in storage_policy.py
    prediction = storage_policy.battery_charging_decision_using_prediction(forecast)
    hours = storage_policy.battery_charging_decision_using_hours(hour)
    remaining = storage_policy.battery_charging_decision_using_remaining(battery_remaining, 100)
    grid = storage_policy.battery_charging_decision_using_grid(grid_price)
    generator = storage_policy.charging_battery_to_a_certain_value(100, battery_remaining, event)

    # Get the electricity demand of each building
    demands = []
    for item in loads:
        demands.append(item["load"])


    # Call the optimizer to allocate enery to each building
    optimizer.grid_price = grid_price
    optimizer.reset_solar()

    buildings = optimizer.allocate_all_buildings(loads, event, grid_price)

    return {"building": buildings, "generator": generator}





def read_json(connection, buffer):
    decoder = json.JSONDecoder()
    while True:
        try:
            text = buffer.decode("utf-8").lstrip()
            data, end = decoder.raw_decode(text)
            return data, text[end:].encode("utf-8")
        except (json.JSONDecodeError, UnicodeDecodeError):
            chunk = connection.recv(4096)
            if not chunk:
                return None, b""
            buffer = buffer + chunk

# Keep track of the hour and battery level
state = {"hour":1, "battery":0}
 # Connect to the server to receive data
with socket.create_connection((HOST, PORT)) as connection:
    # Store any leftover data in case a JASON message arrives in pieces
    buffer = b""
    # Process new data til the connection is off
    while True:
        data, buffer = read_json(connection, buffer)
        # No more data --> exit
        if data is None:
            break
        # Pass the current data to allocation algo
        answer = decide(data, state)
        # Since the socket is in bytes, need to convert python dic into bytes before sending back to the server
        message = json.dumps(answer) + "\n" # py dictionary to string
        connection.sendall (message.encode("utf-8")) # string to bytes