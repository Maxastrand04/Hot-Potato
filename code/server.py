import socket, pygame, threading, json
from settings import *
from debug import debug

class Server():
    def __init__(self):

        self.default_player_data = {
                'X': 5,
                'Y': 2,
                'direction_X': 0,
                'direction_Y': 0, 
                'animation_index': 0,
                'status': 'idle',
            }


        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.format = 'utf-8'
        self.this_is_host = None

        self.my_key = "{}:{}".format(self.host, self.port)
        self.host_key = "{}:{}".format(self.host, self.port)

        self.update = pygame.time.Clock()

    def start_thread(self, function, arguments = None):
        if arguments == None: 
            threading.Thread(target=function).start()
        else:
            threading.Thread(target=function, args=arguments).start()

    def start_listen(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.host)

        self.this_is_host = True

        server.bind((self.host, self.port))
        server.listen(1)


        # Lägger till Hosten som en spelare
        players[self.host_key] = self.default_player_data

        while True:

            client, addr = server.accept()

            print('New connection from {}'.format(addr))

            # Lägger till den tillagda klienten som en spelare
            client_key = '{}:{}'.format(addr[0], addr[1])
            players[client_key] = self.default_player_data

            self.start_thread(self.handle_client, (client, addr))

    def join_server(self):
        
        while True:

            input()
            IP = '192.168.1.5'
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((IP, self.port))

                # Lägger till denna klient som en spelare
                self.my_key = '{}:{}'.format(client.getsockname()[0], client.getsockname()[1])
                players[self.my_key] = self.default_player_data

                # Lägger till Hosten som en spelare
                players[self.host_key] = self.default_player_data
                
                self.start_thread(self.handle_conn, (client, self.my_key))

                break

            except:
                print('felaktig address!')

    def handle_conn(self, client, key):
        while True:
            self.get_data(client, key)

            self.update.tick(SERVER_UPDATE)
        
        client.close()

    def get_data(self, client, key):

        #Börjar med att skicka värden
        if key:

            data_to_send = players[key]
            json_data = json.dumps(data_to_send)
            client.send(json_data.encode(self.format))

            # Därefter tar emot värden
            get_data = client.recv(1024)

            if not get_data:
                client.close()
            else:
                get_data = get_data.decode(self.format)
                get_data = json.loads(get_data)
                for player, values in get_data.items():
                    if not player == key:
                        players[player] = values

    def handle_client(self, client, addr):

        client_key = '{}:{}'.format(addr[0], addr[1])
        
        while True:
            self.send_data(client, client_key)

            self.update.tick(SERVER_UPDATE)
        
        
        client.close()

    def send_data(self, client, key):

        # Börjar med att ta emot
        data_upd = client.recv(1024)
        if not data_upd:
            client.close()
        else:
            data_upd = data_upd.decode(self.format)
            data_upd = json.loads(data_upd)
            players[key] = data_upd

        # Därefter skickar vidare
        json_data = json.dumps(players)
        client.send(json_data.encode(self.format))
