import json
import socket
import optimizer
import storage_policy

hour = 0
HOST = "localhost"
PORT = 8800

def decide(data):
    global hour
    optimizer.reset_solar()
    optimizer.last_hour = (hour == 23)

    buildings = optimizer.allocate_all_buildings(
        data["loads"], data["random_event"], data["grid_price"]
    )
    battery_target = 100
    generator = 0
    if (data["random_event"] != "battery_failure"
        and storage_policy.battery_charging_decision_using_prediction(data["forecast"])
        and storage_policy.battery_charging_decision_using_hours(hour)
        and storage_policy.battery_charging_decision_using_grid(data["grid_price"])
        and storage_policy.battery_charging_decision_using_remaining(
            optimizer.battery_remaining, battery_target
        )):
        generator = storage_policy.charging_battery_to_a_certain_value(
            battery_target, optimizer.battery_remaining, data["random_event"]
        )
    optimizer.charge_battery(generator)
    hour += 1
    return {"buildings": buildings, "generator": generator}


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
            buffer += chunk


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
        answer = decide(data)
        # Since the socket is in bytes, need to convert python dic into bytes before sending back to the server
        message = json.dumps(answer) + "\n" # py dictionary to string
        connection.sendall (message.encode("utf-8")) # string to bytes