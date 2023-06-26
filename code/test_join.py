import requests
import socket

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']
    return ip

server_ip = get_public_ip()
server_port = 8000  # Replace with the desired port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the public IP address and port
server_socket.bind((server_ip, server_port))

# Start listening for incoming connections
server_socket.listen()

print('listening to: ' + server_ip + ':' + server_port)