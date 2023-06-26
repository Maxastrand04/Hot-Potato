import socket, pygame, threading, json
from settings import *
from debug import debug

class Server():
    def __init__(self):

        self.default_player_data = {
                'X': 2,
                'Y': 2,
                'init_X': 2,
                'init_Y': 2,
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

        self.start_draw = False
        self.IP = self.get_public_ip()

    def get_public_ip(self):
        resolver = socket.getaddrinfo('google.com', 80, socket.AF_INET, socket.SOCK_STREAM)
        ip = resolver[0][4][0]
        return ip

    def start_thread(self, function, arguments = None):
        if arguments == None: 
            threading.Thread(target=function).start()
        else:
            threading.Thread(target=function, args=arguments).start()

    def start_listen(self):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.IP)

        self.this_is_host = True

        server.bind((self.IP, self.port))
        server.listen()

        self.start_draw = True


        # Lägger till Hosten som en spelare
        players[self.host_key] = self.default_player_data

        while True:
            self.default_player_data['init_X']

            client, addr = server.accept()

            print('New connection from {}'.format(addr))
            
            # Lägger till den tillagda klienten som en spelare
            client_key = '{}:{}'.format(addr[0], addr[1])

            players[client_key] = self.default_player_data
            init_data = json.dumps(players)
            client.send(init_data.encode(self.format))

            self.start_thread(self.handle_client, (client, addr))

    def join_server(self):
        connected = False
        while True:

            ip = input('IP-Adress: ')
            
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip, self.port))

                connected = True

            except:
                print('felaktig adress!')

            if connected == True:

                # Lägger till denna klient som en spelare
                self.my_key = '{}:{}'.format(client.getsockname()[0], client.getsockname()[1])
                
                self.start_thread(self.handle_conn, (client,))

                break


    def handle_conn(self, client):


        # Hämtar allas postion från servern
        init_data = client.recv(1024)

        if not init_data:
            client.close()
        else:
            init_data = init_data.decode(self.format)
            init_data = json.loads(init_data)
            for player, values in init_data.items():
                players[player] = values

        # Körs sedan för att uppdatera bilden

        self.start_draw = True
        while True:
            self.get_data(client)

            self.update.tick(SERVER_UPDATE)
        
        client.close()

    def get_data(self, client):

        #Börjar med att skicka värden
        if self.my_key:

            data_to_send = players[self.my_key]
            json_data_123123 = json.dumps(data_to_send)
            client.send(json_data_123123.encode(self.format))


            # Därefter tar emot värden
            get_data = client.recv(1024)

            if not get_data:
                client.close()
            else:
                get_data = get_data.decode(self.format)
                get_data = json.loads(get_data)
                #print(get_data)
                for player, values in get_data.items():
                    if not player == self.my_key:
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

