import json
import socket

HOST = "localhost"
PORT = 8800


def decide(data):
    # Replace this function with the team's energy allocation algorithm.
    buildings = []
    for item in data["loads"]:
        buildings.append({"solar": 0, "battery": 0, "grid": item["load"]})
    return {"buildings": buildings, "generator": 0}


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