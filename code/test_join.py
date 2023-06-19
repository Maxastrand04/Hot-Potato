import socket, json

IP = "192.168.1.5"
PORT = 5000
FORMAT = 'utf-8'

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    print('KOPPLAD!')

except:
    print('inte godkänt')


msg = 'hello there'

json_msg = json.dumps(msg)

client.send(json_msg.encode(FORMAT))

