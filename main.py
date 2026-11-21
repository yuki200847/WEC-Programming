import json
import socket

HOST = "localhost"
PORT = 8800


def decide(data):
    # Will Replace this function with the team's energy allocation algorithm.
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


def main():
    with socket.create_connection((HOST, PORT)) as connection:
        buffer = b""
        while True:
            data, buffer = read_json(connection, buffer)
            if data is None:
                break
            answer = decide(data)
            connection.sendall((json.dumps(answer) + "\n").encode("utf-8"))


main()
