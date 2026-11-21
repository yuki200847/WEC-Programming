import json
import socket

names = ["library", "laboratory", "lecture_hall", "student_centre",
         "student_residence", "library", "lecture_hall"]
data = {"random_event": "none", "forecast": "not cloudy",
        "grid_price": 1.2, "loads": []}
for name in names:
    data["loads"].append({"type": name, "load": 20})

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8800))
server.listen(1)
print("Server ready. Run python3 main.py in another terminal.", flush=True)

connection, address = server.accept()
connection.settimeout(10)
connection.sendall((json.dumps(data) + "\n").encode("utf-8"))
answer = json.loads(connection.makefile("r").readline())
print("Answer:", answer)

assert len(answer["buildings"]) == len(names)
for i in range(len(names)):
    building = answer["buildings"][i]
    assert building["solar"] + building["battery"] + building["grid"] == 20
    if names[i] == "lecture_hall":
        assert building["solar"] == 0

print("PASS: basic test completed")
connection.close()
server.close()
